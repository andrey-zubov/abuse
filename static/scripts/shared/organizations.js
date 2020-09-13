export default class Organizations {
  constructor() {
    this.organizations = document.querySelector(".organizations__content");
    this.map = document.querySelector(".organizations__map");
    this.initMapInterval = false;
    this.interval = null;
    this.markers;
    this.map;
    this.test = []; 
    this.YOUR_API = '';
    this.init();
  }

  filterMarkers(showMarkers){
    for (var i = 0; i < this.test.length; i++) {
      this.test[i].setMap(null); //Remove the marker from the map
    }

    this.test = [];

    const activeMarkers =  showMarkers.map((dataMapId)=>{
      const m = this.markers.find(({id})=>{
        return id === +dataMapId
      })
      return m;
    })

    let infowindow = new google.maps.InfoWindow();

    let marker;

    for (let i = 0; i < activeMarkers.length; i++) {
      marker = new google.maps.Marker({
        position: new google.maps.LatLng(activeMarkers[i].lat, activeMarkers[i].lon),
        map: this.map,
      });

      this.test[i] = marker;

      google.maps.event.addListener(
        marker,
        "click",
        (function (marker, i) {
          return function () {
            infowindow.setContent(activeMarkers[i].city);
            infowindow.open(this.map, marker);
          };
        })(marker, i)
      );
    }
  }

  addMarkers() {
    clearInterval(this.interval);

    let locations = [
      {city : "Minsk", lat : 53.953585, lon : 27.545537, id : 123},
      {city : "Gomel", lat :52.441076, lon :28.985343, id: 345},
      {city : "Minsk", lat :53.441076, lon :29.985343, id: 567},
      {city : "Gomel", lat :55.441076, lon :30.985343, id: 789},
    ];

    this.markers = locations;

    this.map = new google.maps.Map(this.map, {
      zoom: 6,
      center: new google.maps.LatLng(locations[0].lat, locations[0].lon),
      mapTypeId: google.maps.MapTypeId.ROADMAP,
    });

    let infowindow = new google.maps.InfoWindow();

    let marker;

    for (let i = 0; i < locations.length; i++) {
      marker = new google.maps.Marker({
        position: new google.maps.LatLng(locations[i].lat, locations[i].lon),
        map: this.map,
      });

      this.test[i] = marker;

      google.maps.event.addListener(
        marker,
        "click",
        ( (marker, i) =>{
          return  () => {
            infowindow.setContent(locations[i].city);
            infowindow.open(this.map, marker);
          };
        })(marker, i)
      );
    }
  }

  initMap() {
    let script = document.createElement("script");
    script.type = "text/javascript";
    script.async = true;
    script.defer = true;
    script.src =
      `https://maps.googleapis.com/maps/api/js?key=${this.YOUR_API}`;
    document.body.insertAdjacentElement("afterbegin", script);

    this.interval = setInterval(() => {
      if (!this.initMapInterval) {
        this.initMapInterval = true;
        this.addMarkers();
      }
    }, 200);
  }

  showOrganization() {
    const isCityData = this.organizations.getAttribute("data-active-city");
    const isSpecData = this.organizations.getAttribute("data-active-spec");
    const isRegion = this.organizations.getAttribute("data-active-region");
    const isDistrict = this.organizations.getAttribute("data-active-district");

    const cityAttr = isCityData ? `[data-city="${isCityData}"]` : '';
    const regionAttr = isRegion ? `[data-region="${isRegion}"]` : '';
    const disctrictAttr = isDistrict ? `[data-district="${isDistrict}"]` : '';

    const attr = cityAttr + regionAttr + disctrictAttr
    const cities = document.querySelectorAll(`.organization-item${attr}`);

    $(".organizations__content").slideUp();
    $(".organization-item").hide();

    let showMarkers = [];

    if(!isSpecData){
      cities.forEach((item)=>{
        const mapId = item.getAttribute('data-map-id');
        showMarkers.push(mapId)
        item.style.display="block";
      })
    }else{
      cities.forEach((item) => {
        let specifications = item.getAttribute("data-spec").split(", ");
  
        let specFind = specifications.find((item) => {
          return item === isSpecData;
        });
  
        if (specFind) {
          const mapId = item.getAttribute('data-map-id');
          showMarkers.push(mapId)
          item.style.display="block";
        }
      });
    }

    if(this.initMapInterval){
      this.filterMarkers(showMarkers);
    }

    $(".organizations__content").slideDown();
  }

  init() {
    $(".organizations__select__specifications").select2({
      closeOnSelect: true,
      placeholder: "Выберите деятельность",
    });

    $(".organizations__select__cities").select2({
      closeOnSelect: true,
      placeholder: "Выберите город",
    });

    $(".organizations__select__region").select2({
      closeOnSelect: true,
      placeholder: "Выберите область",
    });

    $(".organizations__select__district").select2({
      closeOnSelect: true,
      placeholder: "Выберите район",
    });

    $(".organizations__select__specifications").on("select2:close", (e) => {
      const data = e.params.originalSelect2Event?.data.id;
      if(data){
        if(data === "All"){
          this.organizations.removeAttribute('data-active-spec')
        }else{
          this.organizations.dataset.activeSpec = data;
        }
        this.showOrganization();
      }
    });

    $(".organizations__select__region").on("select2:close", (e) => {
      const data = e.params.originalSelect2Event?.data.id;
      if(data){
        if(data === "All"){
          this.organizations.removeAttribute('data-active-region')
        }else{
          this.organizations.dataset.activeRegion = data;
        }
        this.showOrganization();
      }
    });

    $(".organizations__select__district").on("select2:close", (e) => {
      const data = e.params.originalSelect2Event?.data.id;
      if(data){
        if(data === "All"){
          this.organizations.removeAttribute('data-active-district')
        }else{
          this.organizations.dataset.activeDistrict = data;
        }
        this.showOrganization();
      }
    });

    $(".organizations__select__cities").on("select2:close", (e) => {
      const data = e.params.originalSelect2Event?.data.id;
      if(data){
        if(data === "All"){
          this.organizations.removeAttribute('data-active-city')
        }else{
          this.organizations.dataset.activeCity = data;
        }
        this.showOrganization();
      }
    });

    if (this.map) {
      this.initMap();
    }
  }
}
