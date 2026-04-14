// Authentication adapter for Python backend
var authAdapter = {
    token: localStorage.getItem('jwt_token') || null,
    username: localStorage.getItem('username') || null,

    login: function(username, password, callback, errorCallback) {
        var credentials = btoa(username + ':' + password);

        dojo.xhrPost({
            url: "/api/v1/auth/login",
            headers: {
                "Authorization": "Basic " + credentials
            },
            handleAs: "json",
            load: function(data) {
                authAdapter.token = data.access_token;
                authAdapter.username = data.username;
                localStorage.setItem('jwt_token', data.access_token);
                localStorage.setItem('username', data.username);
                if (callback) callback(data);
            },
            error: function(error) {
                console.error("Login failed:", error);
                if (errorCallback) errorCallback(error);
            }
        });
    },

    logout: function() {
        authAdapter.token = null;
        authAdapter.username = null;
        localStorage.removeItem('jwt_token');
        localStorage.removeItem('username');
        window.location.reload();
    },

    isAuthenticated: function() {
        return !!authAdapter.token;
    },

    // Intercept XHR requests to add JWT token
    setupRequestInterceptor: function() {
        var originalXhrGet = dojo.xhrGet;
        var originalXhrPost = dojo.xhrPost;
        var originalXhrPut = dojo.xhrPut;
        var originalXhrDelete = dojo.xhrDelete;

        var addAuthHeader = function(args) {
            if (authAdapter.token) {
                args.headers = args.headers || {};
                args.headers.Authorization = "Bearer " + authAdapter.token;
            }
            // Update URL to use new API prefix
            if (args.url && args.url.startsWith('jaxrs/')) {
                args.url = '/api/v1/' + args.url.substring(6);
            }
            return args;
        };

        dojo.xhrGet = function(args) {
            return originalXhrGet.call(this, addAuthHeader(args));
        };

        dojo.xhrPost = function(args) {
            return originalXhrPost.call(this, addAuthHeader(args));
        };

        dojo.xhrPut = function(args) {
            return originalXhrPut.call(this, addAuthHeader(args));
        };

        dojo.xhrDelete = function(args) {
            return originalXhrDelete.call(this, addAuthHeader(args));
        };
    }
};

// Setup interceptor on page load
if (typeof dojo !== 'undefined') {
    dojo.ready(function() {
        authAdapter.setupRequestInterceptor();
    });
}
