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

    var renderWidget = function(to_user) {
      var promise = getStatus(to_user);
      promise.done(function(status){
        if (status === 'AVAILABLE') {
          // add as friend
          $('#add-as-friend').show();
        } else if (status === 'INVITATION_EXISTS') {
          // Accept?
          $('#accept-invitation').show();
        } else if (status === 'INVITATION_MADE') {
          // requested
          $('#request-sent').show();
        }
      });
      promise.fail(function(){
        return;
      });
    };

    var inviteHandler = function(event) {
      var data = {to_user:event.data.to_user};
      var promise = mymd.ajax.post('/friend/add/', data);
      var btn = $(this);
      btn.attr('disabled', 'disabled')
         .text(btn.attr('processing-text'));
      promise.done(function(result){
        btn.attr('disabled', 'disabled')
           .text(btn.attr('processed-text'));
      });
      promise.fail(function(errorCode, error){
        btn.popover({
          trigger: 'manual',
          title: 'Hoops...',
          content: 'Failed.... Please try again later'
        });
        btn.popover('show');
        btn.attr('disabled', '');
      });
      return false;
    };

    var acceptHandler = function(event) {
      var data = {to_user:event.data.to_user};
      var promise = mymd.ajax.post('/friend/accept/', data);
      var btn = $(this);
      btn.attr('disabled', 'disabled')
         .text(btn.attr('processing-text'));
      btn.siblings('a.action').hide();
      promise.done(function(result){
        var processedText = btn.attr('processed-text');
        btn.parents('form').remove();
        $('#accept-invitation').append('<p>'+processedText+'</p>').fadeOut('slow');
      });
      promise.fail(function(errorCode, error){
        btn.popover({
          trigger: 'manual',
          title: 'Hoops...',
          content: 'Failed.... Please try again later'
        });
        btn.popover('show');
        btn.attr('disabled', '');
        btn.siblings('a.action').show();
      });
      return false;
    };

    var declineHandler = function(event) {
      var data = {to_user:event.data.to_user};
      var promise = mymd.ajax.post('/friend/decline/', data);
      var btn = $(this);
      btn.attr('disabled', 'disabled')
         .text(btn.attr('processing-text'));
      btn.siblings('a.action').hide();
      promise.done(function(result){
        var processedText = btn.attr('processed-text');
        btn.parents('form').remove();
        $('#accept-invitation').append('<p>'+processedText+'</p>').fadeOut('slow');
      });
      promise.fail(function(errorCode, error){
        btn.popover({
          trigger: 'manual',
          title: 'Hoops...',
          content: 'Failed.... Please try again later'
        });
        btn.popover('show');
        btn.attr('disabled', '');
        btn.siblings('a.action').show();
      });
      return false;
    };

    var ignoreHandler = function(event) {
      var data = {to_user:event.data.to_user};
      var promise = mymd.ajax.post('/friend/ignore/', data);
      var btn = $(this);
      btn.attr('disabled', 'disabled')
         .text(btn.attr('processing-text'));
      btn.siblings('a.action').hide();
      promise.done(function(result){
        var processedText = btn.attr('processed-text');
        btn.parents('form').remove();
        $('#accept-invitation').append('<p>'+processedText+'</p>').fadeOut('slow');
      });
      promise.fail(function(errorCode, error){
        btn.popover({
          trigger: 'manual',
          title: 'Hoops...',
          content: 'Failed.... Please try again later'
        });
        btn.popover('show');
        btn.attr('disabled', '');
        btn.siblings('a.action').show();
      });
      return false;
    };

    // public variables
    this.initWidget = function(to_user) {
      renderWidget(to_user);
      $('#add-as-friend .action').click({to_user:to_user}, inviteHandler);
      $('#accept-invitation a[action="accept"]').click({to_user:to_user}, acceptHandler);
      $('#accept-invitation a[action="decline"]').click({to_user:to_user}, declineHandler);
      $('#accept-invitation a[action="ignore"]').click({to_user:to_user}, ignoreHandler);
    };
  } // friends definition ends
  mymd.friends = new friends();
})(jQuery);