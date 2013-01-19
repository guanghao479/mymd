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
    this.getDataObject = function(url, requestData, resultDataKey) {
      var status = new $.Deferred();
      var promise = mymd.ajax.get(url, requestData);
      promise.done(function(result) {
        if (result.error) {
          status.reject(result.error.code, result.error);
        } else if (resultDataKey !== undefined) {
          status.resolve(result[resultDataKey]['status'], result[resultDataKey]);
        } else {
          status.resolve(result);
        }
      });
      promise.fail(function(result) {
        status.reject('NETWORK_FAILED', result);
        console.log('NETWORK_FAILURE: ');
        console.log(result);
      });
      return status.promise();
    };
  }
  mymd.ajax = new ajax();

  function meetup(){
    //private variables
    var renderWidget = function(meetup) {
      var requestData = {
      'meetup': meetup
     }
     var promise = mymd.ajax.getDataObject('/meetup/status/', requestData, 'meetup');
     promise.done(function(status){
      if(status === 'AVAILABLE'){
        //Attend meetup
        $('#meetup-attend').show();
      }else if(status === 'ATTENT'){
        $('#meetup-attent').show();
      }
     });
    promise.fail(function(){
        return;
      });
    };

    var renderAttenders = function(meetup) {
      var requestData = {
        'meetup': meetup
      }
      var promise = mymd.ajax.getDataObject('/meetup/attenders/', requestData, 'attenders');
      promise.done(function(status, attenders){
        var attenders_div = $('#attenders');
        for(var i in attenders){
          attenders_div.append('<p>'+attenders[i].name+'</p>')
        };
      });
    }

    var attendHandler = function(event) {
      var data = {meetup:event.data.meetup};
      var promise = mymd.ajax.post('/meetup/attend/', data);
      var btn = $(this);
      btn.attr('disabled', 'disabled')
        .text(btn.attr('processing-text'));
      promise.done(function(result){
        btn.attr('disabled', 'disabled')
          .text(btn.attr('processed-text'));
      })
      return false;
    }

    this.initWidget = function(meetup) {
      renderWidget(meetup);
      renderAttenders(meetup);
      $('#meetup-attend .action').click({meetup:meetup}, attendHandler);
      //$('#accept-invitation a[action="accept"]').click({to_user:to_user}, acceptHandler);
      //$('#accept-invitation a[action="decline"]').click({to_user:to_user}, declineHandler);
      //$('#accept-invitation a[action="ignore"]').click({to_user:to_user}, ignoreHandler);
    };
  }

  mymd.meetup = new meetup();
  // define mymd.friends to represent user-related friends data
  function friends() {
    // private variables
    var renderWidget = function(to_user) {
      var requestData = {
        'to_user'   : to_user
      }
      var promise = mymd.ajax.getDataObject('/friend/status/', requestData, 'friends');
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

  // define mymd.pins to represent pins specific data
  function pins() {
    // private variables
    var appendPin = function (colid, pin, static_url) {
      var pindiv = $('<div class="pin"></div>');
      if (pin.img) {
        pindiv.append($('<div class="img"><img src="'+static_url+pin.img+'"/></div>'));
      } else if (pin.title) {
        pindiv.append($('<div class="title"><p>'+pin.title+'</p></div>'));
      }
      pindiv.append($('<div class="description"><p>'+pin.description+'</p></div><div class="others"><p>'+pin.likes+' likes '+pin.comments+' comments</p></div>'));
      $('#'+colid).append(pindiv);
    };
    // public variables
    this.initWidget = function(pincols, static_url) {
      var pins = mymd.ajax.getDataObject('/pins/', undefined, 'pins');
      pins.done(function(status, pins){
        var i = 0;
        var colsnum = pincols.length;
        for (i=0;i<pins.length;i++) {
          appendPin(pincols[i%colsnum], pins[i], static_url);
        }
      });
      pins.fail(function(data){
        //TODO: ERROR HANDLING
        return;
      });
    };
  } // friends definition ends
  mymd.pins = new pins();

  function district(){
    var current_city = {};
    var current_district = {};

    this.renderCommunity = function(district_id){
      var requestData = {district_id: district_id};
      if(current_district[district_id]){
        $("#id_community").html(current_district[district_id]);
      }else{
        var community = mymd.ajax.getDataObject('/community/', requestData, 'communities');
        community.done(function(status, community) {
          var options = '';
          for (var i in community) {
            options += '<option value="' + community[i].id + '">'
              + community[i].name + '</option>';
          }
          current_district[district_id] = options;
          $("#id_community").html(options);
        });
      };
    };

    this.renderDistrict = function(city_id){
      var requestData = {city_id: city_id};
      if(current_city[city_id]){
        $("#id_district").html(current_city[city_id]);
        if(current_district[$("#id_district").val()]){
          $("#id_community").html(current_district[$("#id_district").val()]);
        }else{
          $("#id_community").html(current_district[$("#id_district").val()]);
        }
      }else{
        var district = mymd.ajax.getDataObject('/district/', requestData, 'districts');
        district.done(function(status, district) {
          var options = '';
          var district_options = options;
          for (var i in district) {
            district_options += '<option value="' + district[i].id + '">'
              + district[i].name + '</option>';
          }
          current_city[city_id] = district_options;
          $("#id_district").html(district_options);
          mymd.district.renderCommunity($("#id_district").val());
        });
      };
    };


  };
  mymd.district = new district();

})(jQuery);
