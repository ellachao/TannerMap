var map=L.map('mapid').setView([39, 10], 2);

CustomMarker = L.Marker.extend({
   options: { 
       id: null,
       presenter: null,
       year: null,
       major: null,
       org: null
       
   }
});

L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=access_token_here', {
    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
    maxZoom: 18,
    id: 'id_here',
    accessToken: 'access_token_here'
}).addTo(map);

var clusters=L.markerClusterGroup();

function showBox(e){
    $('#details').html(
        'Tanner ID: '+this['options']['id']+'<br>'+
        'Presenter: '+this['options']['presenter']+'<br>'+
        'Class Year: '+this['options']['year']+'<br>'+
	'Major(s): '+this['options']['major']+'<br>'+
	'The name of the organization where the primary presenter interned or were affiliated with: '+this['options']['org']
    );
}

$.getJSON('tanner.json', function(data){
    $.each(data,function(i,obj){
        if (!obj.hasOwnProperty('Additional Presenters')){
            var window='Presenter: '+obj['Primary presenter']+'<br>Title: '+obj['Title of Presentation'];
            var marker=new CustomMarker([obj['location']['lat'],obj['location']['lng']],{
                id: obj['Tanner ID'],
                presenter: obj['Primary presenter'],
                year: obj['Class Year'],
		major: obj['Majors'],
		org: obj['The name of the organization where the primary presenter interned or were affiliated with']
            }).bindPopup(window).on('mouseover', showBox);
            clusters.addLayer(marker);
        }
        else{
            for (i in obj['Additional Presenters']){
                var window='Presenter Info: '+obj['Additional Presenters'][i]['Presenter Info']+'<br>Organization: '+
                    obj['Additional Presenters'][i]['Organization'];
                var marker=L.marker(
                    [obj['Additional Presenters'][i]['location']['lat'],obj['Additional Presenters'][i]['location']['lng']]
                ).bindPopup(window);
                clusters.addLayer(marker);
            }
        }
           
    })
})

map.addLayer(clusters);

