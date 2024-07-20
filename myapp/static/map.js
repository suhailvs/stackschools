const copy = "&copy; <a href='https://www.openstreetmap.org/copyright'>OpenStreetMap</a>";
const layer = L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", { maxNativeZoom: 18, maxZoom: 20, attribution: copy, });
const map = L.map("map", {
  layers: [layer],
  minZoom: 8,
  maxBounds: [
    //south west
    [8.89, 70.47],
    //north east
    [12.27, 80.65]
  ],
});


map.locate()
  .on("locationfound", (e) => map.setView(e.latlng, 13))
  .on("locationerror", () => map.setView([10.59, 76.45], 13));

// map.setMaxBounds(map.getBounds());
function getColor(d) {
  let colors = ['#800026', '#BD0026', '#E31A1C', '#FC4E2A', '#FD8D3C', '#FEB24C', '#FED976',
    '#800026', '#BD0026', '#E31A1C', '#FC4E2A', '#FD8D3C', '#FEB24C', '#FED976',];
  return colors[d - 1];
}

function style(feature) {
  return {
    weight: 2,
    opacity: 1,
    color: 'white',
    dashArray: '3',
    fillOpacity: 0.5,
    fillColor: getColor(feature.properties.DT_CEN_CD)
  };
}


// // Create a layer group
let districtsGroup = L.layerGroup();
let markersGroup = L.layerGroup();

// L.geoJson(districts, { style, }).addTo(districtsGroup);
L.geoJson(districts, {
  onEachFeature: function (feature, layer) {
    L.marker(layer.getBounds().getCenter(), {
      icon: L.divIcon({
        className: 'label',
        html: feature.properties.DISTRICT,
        iconSize: [100, 40]
      })
    }).addTo(districtsGroup);
  },
  style
}).addTo(districtsGroup);



// // We invoke this flow, every time the user stops moving on the map.
async function load_markers() {
  const markers_url = `/map/api/markers/?in_bbox=${map.getBounds().toBBoxString()}`;
  const response = await fetch(markers_url);
  const geojson = await response.json();
  return geojson;
}

async function render_markers() {
  console.log(map.getBounds())
  console.log(map.getZoom())
  map.removeLayer(districtsGroup);
  map.removeLayer(markersGroup);
  if (map.getZoom() > 13) {
    const markers = await load_markers();
    L.geoJSON(markers).bindPopup((layer) => layer.feature.properties.mal_address).addTo(markersGroup);
    markersGroup.addTo(map);
  } else {
    districtsGroup.addTo(map);
  }
}

map.on("moveend", render_markers);

