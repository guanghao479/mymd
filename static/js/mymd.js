if (typeof mymd === 'undefined') {
  var mymd = {};
}
(function($, undefined){
  // define mymd.ajax
  var ajax = function() {
    var call = function(url, type, data) {
      var status = new $.Deferred();
      $.ajax({
        url: url,
        type: type,
        data: data,
        success: function(data) {
          if (data.error) {
            status.reject(data.error.code, data.error);
          } else {
            status.resolve(data);
          }
        },
        error: function(data) {
          status.reject('NETWORK_FAILED', data);
        }
      });
      return status.promise();
    };

    this.get = function(url, data) {
      return call(url, 'GET', data);
    };
    this.post = function(url, data) {
      return call(url, 'POST', data);
    };
  }
  mymd.ajax = new ajax();


  // define mymd.friends to represent user-related friends data
  function friends() {
    // private variables
    var getStatus = function (to_user) {
      var status = new $.Deferred();
      var data = {
        'to_user'   : to_user
      }
      var promise = mymd.ajax.get('/friend/status/', data);
      promise.done(function(data) {
        if (data.error) {
          status.reject(data.error.code, data.error);
        } else {
          status.resolve(data.friends.status, data.friends);
        }
      });
      promise.fail(function(data) {
        status.reject('NETWORK_FAILED', data);
      });
      return status.promise();
    };

    // public variables
    this.renderWidget = function(to_user) {
      var promise = getStatus(to_user);
      promise.done(function(status){
        if (status === 'FRIENDSHIP_EXISTS' || status === 'BLOCKED' 
          || status === 'DECLINED') {
          return;
        } else if (status === 'INVITATION_EXISTS') {
          // Accept?
          $('#accept-invitation').show();
        } else if (status === 'INVITATION_MADE') {
          // requested
          $('#request-sent').show();
        } else {
          // add as friend
          $('#add-as-friend').show();
        }
      });
      promise.fail(function(){
        return;
      });
    };

    this.invite = function(to_user) {
      var status = new $.Deferred();
      data = {to_user:to_user};
      var promise = mymd.ajax.post('/friend/add/', data);
      promise.done(function(result) {
        status.resolve(result);
      });
      promise.fail(function(errorCode, error) {
        status.reject(errorCode, error);
      });
      return status.promise();
    };
  }

  mymd.friends = new friends();
})(jQuery);