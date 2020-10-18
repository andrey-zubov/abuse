export default class Organizations {
  constructor() {
    this.organizations = document.querySelector(".organizations__content");
    this.map = document.querySelector(".organizations__map");
    this.initMapInterval = false;
    this.interval = null;
    this.locations;
    this.markers;
    this.map;
    this.firstArray = [];
    this.YOUR_API = "AIzaSyAknqsh2KRjjBbPy3V7Cahj1j0M7eDITF0";
    this.init();
  }

  setMarkersOnMap(markersArray) {
    let infowindow = new google.maps.InfoWindow();

    let marker;

    for (let i = 0; i < markersArray.length; i++) {
      marker = new google.maps.Marker({
        position: new google.maps.LatLng(
          markersArray[i].lat,
          markersArray[i].lng
        ),
        map: this.map,
      });

      this.firstArray[i] = marker;

      google.maps.event.addListener(
        marker,
        "click",
        ((marker, i) => {
          return () => {
            const content = `<div class="map-popup"><div class="map-popup__content"><p class="map-popup__title">${markersArray[i].title}</p><p class="map-popup__description">${markersArray[i].adress}</p></div></div>`
            infowindow.setContent(content);
            infowindow.open(this.map, marker);
          };
        })(marker, i)
      );
    }

    new MarkerClusterer(this.map, this.firstArray,
      {imagePath: "https://unpkg.com/@googlemaps/markerclustererplus@1.0.3/images/m"})
  }

  filterMarkers(showMarkers) {
    for (var i = 0; i < this.firstArray.length; i++) {
      this.firstArray[i].setMap(null); //Remove the marker from the map
    }
    const activeMarkers = showMarkers.map((dataMapId) => {
      const m = this.markers.find(({ id }) => {
        return id === dataMapId;
      });
      return m;
    });
    
    this.setMarkersOnMap(activeMarkers);
  }

  addMarkers() {
    clearInterval(this.interval);

    this.markers = this.locations;

    this.map = new google.maps.Map(this.map, {
      zoom: 5,
      center: new google.maps.LatLng(
        this.locations[0].lat,
        this.locations[0].lng
      ),
      mapTypeId: google.maps.MapTypeId.ROADMAP,
    });
   
    this.setMarkersOnMap(this.locations);
  }

  initMap() {
    let script = document.createElement("script");
    script.type = "text/javascript";
    script.async = true;
    script.defer = true;
    script.src = `https://maps.googleapis.com/maps/api/js?key=${this.YOUR_API}`;
    document.body.insertAdjacentElement("afterbegin", script);

    this.interval = setInterval(() => {
      if (!this.initMapInterval) {
        if (google) {
          this.initMapInterval = true;
          this.addMarkers();
        }
      }
    }, 200);
  }

  showOrganization() {
    const isCityData = this.organizations.getAttribute("data-active-city");
    const isSpecData = this.organizations.getAttribute("data-active-spec");
    const isRegion = this.organizations.getAttribute("data-active-region");
    const isDistrict = this.organizations.getAttribute("data-active-district");

    const cityAttr = isCityData ? `[data-city="${isCityData}"]` : "";
    const regionAttr = isRegion ? `[data-region="${isRegion}"]` : "";
    const disctrictAttr = isDistrict ? `[data-district="${isDistrict}"]` : "";

    const attr = cityAttr + regionAttr + disctrictAttr;
    const cities = document.querySelectorAll(`.organization-item${attr}`);

    $(".organizations__content").slideUp();
    $(".organization-item").hide();

    let showMarkers = [];

    if (!isSpecData) {
      cities.forEach((item) => {
        const mapId = item.getAttribute("data-map-id");
        showMarkers.push(mapId);
        item.style.display = "block";
      });
    } else {
      cities.forEach((item) => {
        let specifications = item.getAttribute("data-spec").split(", ");

        let specFind = specifications.find((item) => {
          return item === isSpecData;
        });

        if (specFind) {
          const mapId = item.getAttribute("data-map-id");
          showMarkers.push(mapId);
          item.style.display = "block";
        }
      });
    }
    if (this.initMapInterval) {
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
      if (data) {
        if (data === "All") {
          this.organizations.removeAttribute("data-active-spec");
        } else {
          this.organizations.dataset.activeSpec = data;
        }
        this.showOrganization();
      }
    });

    $(".organizations__select__region").on("select2:close", (e) => {
      const data = e.params.originalSelect2Event?.data.id;
      if (data) {
        if (data === "All") {
          this.organizations.removeAttribute("data-active-region");
        } else {
          this.organizations.dataset.activeRegion = data;
        }
        this.showOrganization();
      }
    });

    $(".organizations__select__district").on("select2:close", (e) => {
      const data = e.params.originalSelect2Event?.data.id;
      if (data) {
        if (data === "All") {
          this.organizations.removeAttribute("data-active-district");
        } else {
          this.organizations.dataset.activeDistrict = data;
        }
        this.showOrganization();
      }
    });

    $(".organizations__select__cities").on("select2:close", (e) => {
      const data = e.params.originalSelect2Event?.data.id;
      if (data) {
        if (data === "All") {
          this.organizations.removeAttribute("data-active-city");
        } else {
          this.organizations.dataset.activeCity = data;
        }
        this.showOrganization();
      }
    });

    fetch("http://taac.pythonanywhere.com/api/orgs/")
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        this.locations = data.orgs;
        this.initMap();
      })
      .catch((error) => {
        console.log("error");
      });
  }
}
