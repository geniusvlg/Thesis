import math
from lxml import etree
import json
import unicodedata
import re


def convert_unicode(text):
        if text == '':
            return text
        elif text == None:
            return ''
        text = re.sub(chr(272), 'D', text)
        text = re.sub(chr(273), 'd', text)
        text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore')
        text = text.decode()
        text = text.replace('\n', '')
        text = text.replace('\t', '')
        text = text.replace('\r', '')
        text = text.strip()
        return text

def read_latlng():
    ns={"kml":"http://www.opengis.net/kml/2.2"}
    file = etree.parse("./map.kml")
    county_list = file.xpath('//kml:Placemark', namespaces={"kml":"http://www.opengis.net/kml/2.2"})
    res=[]
    for county in county_list:
        name= county.xpath('./kml:name/text()', namespaces=ns)[0]
        latlngs = county.xpath('.//kml:coordinates/text()', namespaces=ns)[0]
        latlngs=latlngs.split('\n')[1:-1]
        reslatlng=[]
        for latlng in latlngs:
            latlng = latlng.strip().split(',')
            latlng = {"lat": float(latlng[1]),"lng": float(latlng[0])}
            reslatlng.append(latlng)
        res.append({"name": name, "path" : reslatlng})
    return poly_gm2svg(res)



def latLng2point(latLng) :

    return {
        'x': (latLng['lng'] + 180) * (256 / 360),
        'y': (256 / 2) - (256 * math.log(math.tan((math.pi / 4) + ((latLng['lat'] * math.pi / 180) / 2))) / (2 * math.pi))
    }

def poly_gm2svg(gmPaths) :
    point, gmPath, svgPath, svgPaths = [[],[],[],[]]
    minX = 256
    minY = 256
    maxX = 0
    maxY = 0
    res=[]
    for pp in range(len(gmPaths)) :
        gmPath = gmPaths[pp]
        svgPath = []
        for p in range(0,len(gmPath['path']),1):
            gmpoint=gmPath['path'][p]
            point = latLng2point(gmPath['path'][p])
            # point = { 'y': gmpoint['lat'],'x':gmpoint['lng']}
            minX = min(minX, point['x'])
            minY = min(minY, point['y'])
            maxX = max(maxX, point['x'])
            maxY = max(maxY, point['y'])
            svgPath.append(",".join([str(point['x']), str(point['y'])]))
        svgPaths=" ".join(svgPath)
        svgPaths="M" + svgPaths + "Z"
        res.append({
                    "id":"HCM-"+str(pp),
                    "title":convert_unicode(gmPath["name"]),
                    "d": svgPaths
                    })
    defs={
        "leftLongitude":minX,
        "topLatitude":maxY,
        "rightLongitude":maxX,
        "bottomLatitude":minY
    }
    return {"path":res,"defs":defs}

if __name__ == '__main__':
    with open('out.svg','w') as f:
        val= read_latlng()
        json.dump(val,f,indent=4)