search = window.location.search;
if (search.indexOf("code=") < 0) {
    alert("Please Login First!");
    window.location = "https://longhaomin.auth.us-east-1.amazoncognito.com/login?response_type=code&client_id=4a242ijerctjvohfmlmsf0d6e9&redirect_uri=https://s3.amazonaws.com/longhaominnb/test1/index.html";
}
code = search.substr(search.indexOf("code=")+5);
var id_token;
var authType = 'AWS_IAM';
$.ajax({
    type: 'POST',
    url: 'https://longhaomin.auth.us-east-1.amazoncognito.com/oauth2/token',
    dataType : "json",
    async: false,
    data: {
        "grant_type": "authorization_code",
        "client_id": "4a242ijerctjvohfmlmsf0d6e9",
        "code": code,
        "redirect_uri": "https://s3.amazonaws.com/longhaominnb/test1/index.html"
    },
    success: function (response) {
        id_token = response.id_token;
    }
});

AWS.config.region = 'us-east-1';
var cognitoidentity = new AWS.CognitoIdentity({
  httpOptions:{
	xhrAsync: false
  }
});
var params1 = {
  IdentityPoolId: 'us-east-1:f24056ce-8e56-4894-bdbf-e51645c4eb05',
  AccountId: '424423117805',
  Logins: {
	"cognito-idp.us-east-1.amazonaws.com/us-east-1_4b1sooJwl": id_token
  }
};

var id;
cognitoidentity.getId(params1, function(err, data) {
  if (err) console.log(err, err.stack);
  else {
	id=data.IdentityId;
  }
});

var params2 = {
  IdentityId: id,
  Logins: {
    'cognito-idp.us-east-1.amazonaws.com/us-east-1_4b1sooJwl': id_token
  }
};
var credentials;

cognitoidentity.getCredentialsForIdentity(params2, function(err, data) {
  if (err) console.log(err, err.stack); // an error occurred
  else  {
	credentials = data.Credentials; // successful response
  }
});
//alert(credentials.AccessKeyId);
//alert(credentials.SecretKey);
//alert(credentials.SessionToken);
AWS.config.credentials = credentials;

var apigClientFactory = {};
var message0 = "";
var message1 = "hi";
var params = {
      // This is where any modeled request parameters should be added.
      // The key is the parameter name, as it is defined in the API in API Gateway.
};

var body = {
      // This is where you define the body of the request,
    e:message0
};

var additionalParams = {
    // If there are any unmodeled query parameters or headers that must be
      //   sent with the request, add them here.
  headers: {
  },
  queryParams: {
  }
};
apigClientFactory.newClient = function (config) {
    var apigClient = { };
    if(config === undefined) {
        config = AWS.config;
    }
    if(config.credentials.AccessKeyId === undefined) {
        config.credentials.AccessKeyId = '';
    }
    if(config.credentials.SecretKey === undefined) {
        config.credentials.SecretKey = '';
    }
    if(config.apiKey === undefined) {
        config.apiKey = '';
    }
    if(config.credentials.SessionToken === undefined) {
        config.credentials.SessionToken = '';
    }
    if(config.region === undefined) {
        config.region = 'us-east-1';
    }
    //If defaultContentType is not defined then default to application/json
    if(config.defaultContentType === undefined) {
        config.defaultContentType = 'application/json';
    }
    //If defaultAcceptType is not defined then default to application/json
    if(config.defaultAcceptType === undefined) {
        config.defaultAcceptType = 'application/json';
    }


    // extract endpoint and path from url
    var invokeUrl = 'https://w6py4l6hwc.execute-api.us-east-1.amazonaws.com/prod';
    var endpoint = /(^https?:\/\/[^\/]+)/g.exec(invokeUrl)[1];
    //alert(invokeUrl);
   // alert(endpoint);
    var pathComponent = invokeUrl.substring(endpoint.length);
    //alert(pathComponent);
    var sigV4ClientConfig = {
        accessKey: config.credentials.AccessKeyId,
        secretKey: config.credentials.SecretKey,
        sessionToken: config.credentials.SessionToken,
        serviceName: 'execute-api',
        region: config.region,
        endpoint: endpoint,
        defaultContentType: config.defaultContentType,
        defaultAcceptType: config.defaultAcceptType
    };

    if (sigV4ClientConfig.accessKey !== undefined && sigV4ClientConfig.accessKey !== '' && sigV4ClientConfig.secretKey !== undefined && sigV4ClientConfig.secretKey !== '') {
        authType = 'AWS_IAM';
    }
    //authType = 'NONE';

    var simpleHttpClientConfig = {
        endpoint: endpoint,
        defaultContentType: config.defaultContentType,
        defaultAcceptType: config.defaultAcceptType
    };
    //alert(sigV4ClientConfig.accessKey);
    var apiGatewayClient = apiGateway.core.apiGatewayClientFactory.newClient(simpleHttpClientConfig, sigV4ClientConfig);
    //alert(authType);
    apigClient.chatbotPost = function (params, body, additionalParams) {
        if(additionalParams === undefined) { additionalParams = {}; }

        apiGateway.core.utils.assertParametersDefined(params, ['body'], ['body']);

        var chatbotPostRequest = {
            verb: 'post'.toUpperCase(),
            path: pathComponent + uritemplate('/chatbot').expand(apiGateway.core.utils.parseParametersToObject(params, [])),
            headers: apiGateway.core.utils.parseParametersToObject(params, []),
            queryParams: apiGateway.core.utils.parseParametersToObject(params, []),
            body: body
        };


        return apiGatewayClient.makeRequest(chatbotPostRequest, authType, additionalParams, config.apiKey);
    };
    return apigClient;
};
var apigClient = apigClientFactory.newClient();
(function(){

  var chat = {
    messageToSend: '',
    messageResponses: [
      'Why did the web developer leave the restaurant? Because of the table layout.',
      'How do you comfort a JavaScript bug? You console it.',
      'An SQL query enters a bar, approaches two tables and asks: "May I join you?"',
      'What is the most used language in programming? Profanity.',
      'What is the object-oriented way to become wealthy? Inheritance.',
      'An SEO expert walks into a bar, bars, pub, tavern, public house, Irish pub, drinks, beer, alcohol'
    ],
    init: function() {
      this.cacheDOM();
      this.bindEvents();
      this.render();
    },
    cacheDOM: function() {
      this.$chatHistory = $('.chat-history');
      this.$button = $('button');
      this.$textarea = $('#message-to-send');
      this.$chatHistoryList =  this.$chatHistory.find('ul');
    },
    bindEvents: function() {
      this.$button.on('click', this.addMessage.bind(this));
      this.$textarea.on('keyup', this.addMessageEnter.bind(this));
    },
    render: function() {
      this.scrollToBottom();
      if (this.messageToSend.trim() !== '') {
        var template = Handlebars.compile( $("#message-template").html());
        var context = {
          messageOutput: this.messageToSend,
          time: this.getCurrentTime()
        };

        this.$chatHistoryList.append(template(context));
        this.scrollToBottom();
        this.$textarea.val('');

        // responses
        var templateResponse = Handlebars.compile( $("#message-response-template").html());
        var contextResponse = {
          response: "Hi",
          time: this.getCurrentTime()
        };

        setTimeout(function() {
          this.$chatHistoryList.append(templateResponse(contextResponse));
          this.scrollToBottom();
        }.bind(this), 1500);

      }

    },
    render1: function(msg) {
      this.scrollToBottom();
      if (this.messageToSend.trim() !== '') {
        var template = Handlebars.compile( $("#message-template").html());
        var context = {
          messageOutput: this.messageToSend,
          time: this.getCurrentTime()
        };

        this.$chatHistoryList.append(template(context));
        this.scrollToBottom();
        this.$textarea.val('');

        // responses
        var templateResponse = Handlebars.compile( $("#message-response-template").html());
        var contextResponse = {
          response: msg,
          time: this.getCurrentTime()
        };
        setTimeout(function() {
          this.$chatHistoryList.append(templateResponse(contextResponse));
          this.scrollToBottom();
        }.bind(this), 1500);

      }

    },
    postmessage: function(send_msg) {
        //body1 = {
         // messages:[{
          //    type: "none",
           //   unstructured: {
             //     id: "007",
               //   text: send_msg,
                 // timestamp: this.getCurrentTime
             // }
          //}]
       // };
      body1 = {
        userId: code,
        message: send_msg
      }
      var temp = this;
      apigClient.chatbotPost(params, body1, additionalParams)
        .then(function(result){
         // alert("hahaha");
          //alert(result.data.message);
          temp.render1(result.data);
          return result.data;
        }).catch( function(result){
            //This is where you would put an error callback
            alert("Please Login First!");
            window.location = "https://longhaomin.auth.us-east-1.amazoncognito.com/login?response_type=code&client_id=4a242ijerctjvohfmlmsf0d6e9&redirect_uri=https://s3.amazonaws.com/longhaominnb/test1/index.html";

            return "ERROR";
        });
    },
    addMessage: function() {

      this.messageToSend = this.$textarea.val();
      var msg = this.postmessage(this.messageToSend);
      //this.render1(msg);
    },
    addMessageEnter: function(event) {
        // enter was pressed
        if (event.keyCode === 13) {
          this.addMessage();
        }
    },
    scrollToBottom: function() {
       this.$chatHistory.scrollTop(this.$chatHistory[0].scrollHeight);
    },
    getCurrentTime: function() {
      return new Date().toLocaleTimeString().
              replace(/([\d]+:[\d]{2})(:[\d]{2})(.*)/, "$1$3");
    },
    getRandomItem: function(arr) {
      return arr[Math.floor(Math.random()*arr.length)];
    }

  };

  chat.init();

  var searchFilter = {
    options: { valueNames: ['name'] },
    init: function() {
      var userList = new List('people-list', this.options);
      var noItems = $('<li id="no-items-found">No items found</li>');

      userList.on('updated', function(list) {
        if (list.matchingItems.length === 0) {
          $(list.list).append(noItems);
        } else {
          noItems.detach();
        }
      });
    }
  };

  searchFilter.init();

})();
