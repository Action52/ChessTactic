function BiographyObject(myTitle, myDescription, myYearBorn, myYearDead) {

    this.title = myTitle;
    this.description = myDescription;
    this.yearborn = myYearBorn;
    this.yeardead = myYearDead;
    this.token = sessionStorage.token;
    this.urlImage = sessionStorage.urlImage;
    this.toJsonString = function () { return JSON.stringify(this); };

};


function addBiographyDemo()
{
	try
  {


    alert("token : " + sessionStorage.token);

  	var myData = new BiographyObject(
     $("#title").val(),
     $("#description").val(),
     $("#yearborn").val(),
     $("#yeardead").val()
     );
  	alert(myData.toJsonString());

  	 jQuery.ajax({
           type: "POST",
           url: "/_ah/api/biography_api/v1/biography/insert",
           data: myData.toJsonString(),
           contentType: "application/json; charset=utf-8",
           dataType: "json",
           success: function (response) {
                // do something
                alert (response.code + " " + response.message);
           },

           error: function (error) {
                // error handler
                alert("error :" + error.message)
           }

       });

   }
   catch(error)
   {
    alert(error);
   }

}


function TokenObject() {

    this.tokenint = sessionStorage.token;
    this.toJsonString = function () { return JSON.stringify(this); };

};


function getBiographyList()
{
  try
  {


    //alert("token : " + sessionStorage.token);

    var myData = new TokenObject();

    alert(myData.toJsonString());

     jQuery.ajax({
           type: "POST",
           url: "/_ah/api/biography_api/v1/biography/list",
           data: myData.toJsonString(),
           contentType: "application/json; charset=utf-8",
           dataType: "json",
           success: function (response) {
                // do something

                alert (response.data);
           },

           error: function (error) {
                // error handler
                alert("error :" + error.message)
           }

       });

   }
   catch(error)
   {
    alert(error);
   }

}

function uploadDemo()

{

    var file_data = $("#uploaded_file").prop("files")[0];
    var form_data = new FormData();
    form_data.append("uploaded_file", file_data)

    jQuery.support.cors = true;
    try
    {
     jQuery.ajax({
                url: "/up",
                dataType: 'text',
                cache: false,
                contentType: false,
                processData: false,
                data: form_data,
                type: 'post',
                crossDomain: true,
                success: function(response){

                                document.getElementById("preview").src=response;

                                sessionStorage.urlImage = response;

                                document.getElementById("url_photo").value = response;
                }
      });
    }
    catch(e)
    {
      alert("error : " +  e);
     }
}
