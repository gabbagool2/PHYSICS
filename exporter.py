import matplotlib.pyplot as plt
import constants
#this handles the exporting for using on google earth Google GEMINI WROTE THIS FUNCTION
def export_kml(sailors):
    print("\n🗺️ --- GENERATING GOOGLE EARTH MAPS ---")
    for sailor in sailors:
        # Join the list of daily coordinates into a single string separated by spaces
        coords_string = " ".join(sailor['track'])
        filename = f"{sailor['name'].replace(' ', '_')}_Route.kml"
        
        # The KML Template
        kml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <name>{sailor['name']}'s Journey</name>
    <Style id="routeStyle">
      <LineStyle>
        <color>ff2dc0fb</color>
        <width>4</width>
      </LineStyle>
    </Style>
    <Placemark>
      <name>{sailor['name']} Track</name>
      <styleUrl>#routeStyle</styleUrl>
      <LineString>
        <tessellate>1</tessellate>
        <coordinates>
          {coords_string}
        </coordinates>
      </LineString>
    </Placemark>
  </Document>
</kml>
"""
        # Write the file to your hard drive
        with open(filename, 'w') as file:
            file.write(kml_content)
            
        print(f"📁 Saved map file: {filename}")



