function getAllData(){
	getData();
	getBiographiesData();
	getBlogsData();
	getOpeningsData();
}
function getData()
{

	sessionStorage.empresa = "outlook";

    jQuery.support.cors = true;
    try
    {
     $.ajax({
        url: "/getTactics",
        dataType: 'json',
        cache: false,
        contentType: false,
        processData: true,
        data: {empresa: sessionStorage.empresa},
        type: 'get',
        crossDomain: true,
        success: function(response) {
	  tactics = response;
          //alert(response);
          tactics.forEach(function (tactic)
          {
             var nombre = "<div class='col-md-3' " +
  			" '> " +
                        "<img src='" +tactic.urlImage + "'" +
                        " class='' alt='team img' height='200' width='200'" +
                        " >" +
                        " <div class='section-title wow bounceIn'> " +
                        "<h4><strong>" +tactic.title + "</strong></h4>" +
                        "<br>" +tactic.description + "" +
                        "<br>Category: " +tactic.category + "" +
                        "<br>Solution: " +tactic.solution + "" +
                        "</div>" +
                        "</div>"
                       $("#tactics").append(nombre);
                });

 	 }
        });




    }
 catch(e)
    {
      alert("error : " +  e);
     }
}



function getBiographiesData()
{

	sessionStorage.empresa = "outlook";

    jQuery.support.cors = true;
    try
    {
     $.ajax({
        url: "/getBiographies",
        dataType: 'json',
        cache: false,
        contentType: false,
        processData: true,
        data: {empresa: sessionStorage.empresa},
        type: 'get',
        crossDomain: true,
        success: function(response) {
	  biographies = response;
          //alert(response);
          biographies.forEach(function (biography)
          {
             var nombre = "<div class='col-md-3' " +
  			" '> " +
                        "<img src='" +biography.urlImage + "'" +
                        " class='' alt='team img' height='200' width='200'" +
                        " >" +
                        " <div class='section-title wow bounceIn'> " +
                        "<strong><h4>" +biography.title + "</h4></strong>" +
                        "<br>" +biography.description + "" +
                        "<br>Year born: " +biography.yearborn + "" +
                        "<br>Year dead: " +biography.yeardead + "" +
                        "</div>" +
                        "</div>"
                       $("#biographies").append(nombre);
                });

 	 }
        });

    }
 catch(e)
    {
      alert("error : " +  e);
     }
}



function getBlogsData()
{

	sessionStorage.empresa = "outlook";

    jQuery.support.cors = true;
    try
    {
     $.ajax({
        url: "/getBlogs",
        dataType: 'json',
        cache: false,
        contentType: false,
        processData: true,
        data: {empresa: sessionStorage.empresa},
        type: 'get',
        crossDomain: true,
        success: function(response) {
	  blogs = response;
          //alert(response);
          blogs.forEach(function (blog)
          {
             var nombre = "<div class='col-md-3' " +
  			" '> " +
                        "<img src='" +blog.urlImage + "'" +
                        " class='' alt='team img' height='200' width='200'" +
                        " >" +
                        "<div class='section-title wow bounceIn'> " +
                        "<strong><h4>" +blog.title + "</h4></strong>" +
                        "<br>" +blog.description + "" +
                        "<br>Author: " +blog.author + "" +
                        "<br>Date: " +blog.date + "" +
                        "</div>" +
                        "</div>"
                       $("#blogs").append(nombre);
                });

 	 }
        });

    }
 catch(e)
    {
      alert("error : " +  e);
     }
}




function getOpeningsData()
{

	sessionStorage.empresa = "outlook";

    jQuery.support.cors = true;
    try
    {
     $.ajax({
        url: "/getOpenings",
        dataType: 'json',
        cache: false,
        contentType: false,
        processData: true,
        data: {empresa: sessionStorage.empresa},
        type: 'get',
        crossDomain: true,
        success: function(response) {
	  openings = response;
          //alert(response);
          openings.forEach(function (opening)
          {
             var nombre = "<div class='col-md-3' " +
  			" '> " +
                        "<img src='" +opening.urlImage + "'" +
                        " class='' alt='team img' height='200' width='200'" +
                        " >" +
                        "<div class='section-title wow bounceIn'> " +
                        "<strong><h4>" +tactic.title + "</h4></strong>" +
                        "<br>" +opening.description + "" +
                        "<br>Movements: " +opening.movements + "" +
                        "<br>Players: " +opening.players + "" +
                        "</div>" +
                        "</div>"
                       $("#openings").append(nombre).listview('refresh');
                });

 	 }
        });

    }
 catch(e)
    {
      alert("error : " +  e);
     }
}
