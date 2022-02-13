from flask import Flask,render_template,request,jsonify,url_for, flash
from werkzeug.utils import secure_filename
import os
import pickle
import time
import base64
import threading
from flasksolution.fuzzysearchmodule import FuzzySearchEngine as FSE
from pathlib import Path
from pdfminer.high_level import extract_pages

# x=FSE("searchphrase")
# path = Path("filepath").expanduser()
# pages = extract_pages(path)
# x.show_ltitem_hierarchy(pages)
# print(x.allmatches)

UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = {'pdf'}

FuzzySearchResults={}

infopath="infofile.pickle"
info=[]  #file and time
if(os.path.isfile(infopath)):
    if os.path.getsize(infopath) > 0:
        with open(infopath, 'rb') as data:

            info = pickle.load(data)
            data.close()

else:
    with open(infopath,'wb') as output:
        pickle.dump(info,output)
        output.close()
#TODO open another thread and check every hour if there are any files that are older than an hour  AND check if there are any old files in fuzzy searched file

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
nummatches=5
def formtable(results):
    arr = {}
    i = 0
    while (i < len(results['matches'])):
        if (results['matches'][i]['match'] in arr):
            pages = arr[results['matches'][i]['match']][0] + [results['matches'][i]['page']]
            # print(pages)
            # # print(type(pages))
            # print(set(pages))
            pages = list(set(pages))
            # pages=set(pages)
            arr[results['matches'][i]['match']] = [pages, results['matches'][i]['matchesonpage'] +
                                                   arr[results['matches'][i]['match']][1]]
        else:
            arr[results['matches'][i]['match']] = [[results['matches'][i]['page']],
                                                   results['matches'][i]['matchesonpage']]
        i += 1
    return arr

def arrelement(arr,position):
    arr2=[]
    for n in arr:
        arr2.append(n[position])
    return arr2
def FormatToJson(input):
    output={}
    output['nummatches']=len(input)
    i=0
    arr=[]
    lenght=len(input)
    while (i < lenght):
        arr.append(i)
        i+=1
    i = 0
    output['matches'] = dict.fromkeys(arr)
    uniquematches=[]
    for n in input:
        if(n[0] not in uniquematches):
            uniquematches.append(n[0])
    #print(uniquematches)
    UniqueMatchesExtended=[]
    for n in uniquematches:
        for j in input:
            if(j[0]==n):

                if((n not in arrelement(UniqueMatchesExtended,0))):
                    UniqueMatchesExtended.append([n,j[1],1])
                else:
                    UniqueMatchesExtended[uniquematches.index(n)]=[n,UniqueMatchesExtended[uniquematches.index(n)][1],UniqueMatchesExtended[uniquematches.index(n)][2]+1]

    #print(UniqueMatchesExtended)
    while(i<lenght):
        output['matches'][i]=dict.fromkeys(['match','page','matchesonpage'])
        output['matches'][i]['match'] = input[i][0]
        output['matches'][i]['page']=input[i][1]
        output['matches'][i]['matchesonpage']=1
        i+=1
    return output

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
# def convert_and_save(b64_string):
#
#     b64_string += '=' * (-len(b64_string) % 4)  # restore stripped '='s
#
#     string = b'{b64_string}'
#
#     with open("tmp/imageToSave.png", "wb") as fh:
#         fh.write(base64.decodebytes(string))



def convert_and_save(b64_string,filename):
    if(allowed_file(filename+".pdf")):
        with open(filename+".pdf", "wb") as fh:
            fh.write(base64.decodebytes(b64_string.encode()))
        with open(infopath, 'wb') as output:
            pickle.dump(info.append([filename,time.time()]), output)
import json
@app.route('/upload', methods=['POST'])
def upload():
    #print("boa")
    #print(request.get_data(as_text=True)[:60])
    data = request.get_json()
    #data= json.loads(request.get_data(as_text=True)[:40][:-1])
    id=data[:9]
    print(id)
    data=data[38:][:-1]   #first 9 = id  (28)
    print(data[:30])
    #print(data[-10:])
    #print(data)

    if data is None:
        print("No valid request body, json missing!")
        return jsonify({'error': 'No valid request body, json missing!'})
    else:

        #img_data = data['img']

        # this method convert and save the base64 string to image
        convert_and_save(data,filename=str(id))
        return jsonify("successfully downloaded data!")
# @app.route('/process_blob', methods=['POST'])
# def processblob():
#     if request.method == 'POST':
#         print('boa')
#         # check if the post request has the file part
#         if 'file' not in request.files:
#             return "no file"
#             #flash('No file part')
#             #return redirect(request.url)
#         file = request.files['file']
#         # If the user does not select a file, the browser submits an
#         # empty file without a filename.
#         if file.filename == '':
#             return "filename is empty"
#             #flash('No selected file')
#             #return redirect(request.url)
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             return "successfully downloaded: "+filename


def thread_function(id,searchphrase):
    print(id)
    print(searchphrase)

    print("Thread {}: starting".format(id))
    x=FSE(searchphrase)
    path = Path(id).expanduser()  #PATH!!! upload !!!1 TODO add download directory
    pages = extract_pages(path)
    x.show_ltitem_hierarchy(pages)
    print(x.allmatches)
    FuzzySearchResults[id]=formtable(x.allmatches)
    #time.sleep(2)
    print("Thread {}: finishing".format(id))



@app.route('/process_qtc', methods=['POST', 'GET'])
def process_qt_calculation():
    if request.method == "POST":
        qtc_data = request.get_json()
        #TODO add new thread to fuzzy search and when ready send to web tableform
        print(qtc_data)
        #print(qtc_data[0]['input'])
        #print(qtc_data[0]['id'])
        x = threading.Thread(target=thread_function, args=(qtc_data['id'],qtc_data[0]['input'],))
        x.start()

        #TODO add a function waiting for request from setInterval and if a key with an id exists in FuzzySearchResults then return data
    # results = {'nummatches': 3,
    #            'matches': {
    #                0:{
    #                'match':"Important",
    #                'page':7,
    #                'matchesonpage':2
    #                       },
    #                1: {
    #                    'match': "Omportant",
    #                    'page': 2,
    #                    'matchesonpage': 1
    #                },
    #                2: {
    #                    'match': "Important",
    #                    'page': 5,
    #                    'matchesonpage': 6
    #                }
    #            },
    #            }
    # results['tablematch']=formtable(results)
    #print(results)
    results="Your pdf is being processed"
    return jsonify(results)

@app.route("/", methods=['post','get'])
def hello_world():
    message = '1'
    if request.method == 'POST':
        message = request.form.get('searchtext')  # access the data inside
    print(message)
    return render_template("index.html",examplevariable="test")  #templates folder
    return '''<!DOCTYPE html>
<!--
Copyright 2012 Mozilla Foundation

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Adobe CMap resources are covered by their own copyright but the same license:

    Copyright 1990-2015 Adobe Systems Incorporated.

See https://github.com/adobe-type-tools/cmap-resources
-->
<html dir="ltr" mozdisallowselectionprint>
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
    <meta name="google" content="notranslate">
    <title>PDF.js viewer</title>

    
    <link rel="stylesheet" href="/static/web/viewer.css">

<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js">
</script>
    <link rel="shortcut icon" type="image/jpg" href="/static/web/ico.ico">
	<link href="/static/fontawesome5.15.4/css/all.css" rel="stylesheet">
<!-- This snippet is used in production (included from viewer.html) -->
<link rel="resource" type="application/l10n" href="/static/web/locale/locale.properties">
<script src="/static/build/pdf.js"></script>


  <script src="/static/web/viewer.js"></script>
<script type="text/javascript">

function infobtn(){
	if(document.getElementById('textaboutfuzzysearch').style.display!='block'){
  			document.getElementById('textaboutfuzzysearch').style.display='block';
		}else{
			document.getElementById('textaboutfuzzysearch').style.display='none';
		}
}

function getmatches(inputstring){
	//figure out for this to actually work, now i am sending a test string
	//number of matches, [match, page, matchesonpage], [match, page, matchesonpage]
	var dict = []; // create an empty array

	dict.push({
    	numberofmathes: 5
	});

	// alert(dict[0].key);
	// alert(dict.length);
	dict.push({
    	match:   "Important",
    	page: 4,
    	matchesonpage: 2
	});
	dict.push({
    	match:   "Importont",
    	page: 2,
    	matchesonpage: 1
	});
	dict.push({
    	match:   "Omportant",
    	page: 13,
    	matchesonpage: 2
	});

	// alert(dict[0].numberofmathes);
	// alert(dict[1].match);
	// alert(dict[1].page);
	// alert(dict[1].matchesonpage);

	// alert(dict[1].value);
	// alert(dict.length);
}

sessionStorage.setItem('sessionID', Math.random().toString(36).substr(2, 9));
console.log(sessionStorage.getItem('sessionID'));

</script>
<style type="text/css">
	#topMenu{
		color:white;
		margin-top: 1.5%;
		margin-left: 2%;
		padding-bottom: 0.5%;
	}
	#infoicon{
		color: white;
		font-size: 2em;
		vertical-align: middle;
	}
	#btnlabeltext{
		vertical-align: middle;
		margin-left: 0.5%;
		user-select: none;
		font-size: 1.2em;
		font-weight: 600;
		cursor: pointer;
	}
	#btnlabeltext:hover{
		color: #c7c7c7;

	}
	#infobox{
		display: block;
		margin-top: 0.5%
	}
	#infobox:hover{
/*		cursor: pointer;
*/	/*	color: #c7c7c7;*/
	}
	#infoicon:hover{
		color: #c7c7c7;
		cursor: pointer;
	}
	#searchinput{
		padding: 0.5%;
		color: white;
		font-size: 1.5em;
		border-radius: 6px;
		background-color: #3b3d44;
		border:none;
	}
	#searchinput:hover {
	  /*background-color: rgba(0, 0, 0, 0.236);*/
	  border-radius: 8px;
	  box-shadow: 0px 0px 10px rgba(255, 255, 255, 0.5);
	  box-shadow: 0px 0px 10px 6px rgba(0, 0, 0, 0.312);
	 /* cursor: pointer;*/
	}
	.searchbtn{
		margin-left: 1%;
		padding: 0.5%;
		color: white;
		font-size: 1.5em;
		border-radius: 6px;
		background-color: #3b3d44;
		border:none;
		cursor: pointer;


	}
	/*#searchbtn:hover {
	  /*background-color: rgba(0, 0, 0, 0.236);*/
	/*  border-radius: 8px;
	  box-shadow: 0px 0px 3px rgba(255, 255, 255, 0.2);
	  box-shadow: 0px 0px 10px 6px rgba((20, 3, 3, 0.112);
	  cursor: pointer;
	}*/
	.searchbtn:active {
	  /*background-color: rgba(0, 0, 0, 0.236);*/
	  border-radius: 8px;
	  box-shadow: 0px 0px 10px rgba(255, 255, 255, 0.5);
	  box-shadow: 0px 0px 10px 6px rgba((101, 93, 93, 0.312);
	  cursor: pointer;
	}

/*table {
  font-family: arial, sans-serif;
  border-collapse: collapse;
  width: 100%;
  background-color: white;
}

td, th {
  border: 1px solid #dddddd;
  text-align: left;
  padding: 8px;
}

tr:nth-child(even) {
  background-color: #dddddd;
}
body{
	background-color: blue;
}

h2{
	background-color: blue;
	color: white;
}*/
/*#htmlt{
	background-color: white;
}*/

</style>
<style type="text/css">
table {
  font-family: arial, sans-serif;
  border-collapse: collapse;
/*  width: 100%;
*/  background-color: #3b3b3b;
  margin-top: 1%;
}

td, th {
  border: 1px solid #dddddd;
  text-align: left;
  padding: 8px;
}

tr:nth-child(even) {
  background-color: #3b3b3b;
}
important
3 importont
2 umportant

</style>
<style type="text/css">
	.pagelink{
		text-decoration: underline;
		color: #9b9bff;
		cursor: pointer;
	}
	.pagelink:hover{
		color: #6969eb;
	}
	#searchtable{
			font-size: 1.3em;

	}
#searchall{
  margin-top: 1%;
}
</style>

<script type="text/javascript">
	function openpage(pagenum){
			//document.getElementById('pageNumber').value=pagenum;
			//toolbar.setPageNumber(2);
			PDFViewerApplication.pdfLinkService.goToPage(pagenum);
	}
	function search(searchtext){
    if(document.getElementById('viewFind').classList.contains("toggled")){
    //document.getElementById('viewFind').click();
    }else{
    document.getElementById('viewFind').click();
    }
    document.getElementById('findInput').value=searchtext;
    document.getElementById('findHighlightAll').click();       //do something about this later
    document.getElementById('findHighlightAll').click();

    // document.getElementById('findNext').click();
    // document.getElementById('findPrevious').click();

			//document.getElementById('viewFind').toggle;
      // document.getElementById("viewFind").classList.add("toggled");
      // document.getElementById("viewFind").setAttribute("aria-expanded", "true");
      // document.getElementById("findbar").remove("hidden");
      // document.getElementById("findInput").select();
      // document.getElementById("findInput").focus();
			// alert('2');
	}

    //   this.toggleButton.classList.add("toggled");
    //   this.toggleButton.setAttribute("aria-expanded", "true");
    //   this.bar.classList.remove("hidden");
    // }

    // this.findField.select();
    // this.findField.focus();
function linkpages(arr){
    var arr2=[];
    for(var i=0; i<arr.length;i++){
        //console.log(arr[i]);
        arr2.push("<span class='pagelink' onclick='openpage("+arr[i]+")'> "+arr[i] +"</span>");
    }
    
    
    
    //arr.forEach(element){
    //    arr2.push("21");
//        arr2.push("<span onclick='openpage("+element+")'> "+element +"</span>")
    //    console.log(element)
    //);
    //}
    //console.log(arr2);
    return arr2
}

function placeintable(result) {
    console.log("Result2:");
    console.log(result);
    if(result['nummatches']!=0){
    document.getElementById("searchresblock").style.display="block";
    
    //for (var i = 0; i<result['nummatches']; i++) {
    //    const tr = document.createElement("tr");
    //    const thnum = document.createElement("th");
    //   const thmatch = document.createElement("th");
    //    const thpage = document.createElement("th");
    //    const thmatchesnum = document.createElement("th");
    //    thnum.innerHTML=i+1;
    //    thmatch.innerHTML=result['matches'][i]['match'];
    //    thpage.innerHTML=result['matches'][i]['page'];
    //    thmatchesnum.innerHTML=result['matches'][i]['matchesonpage'];
    //    tr.setAttribute('id','tr'+i.toString());
    //    document.getElementById("searchtablebody").appendChild(tr); 
    //    document.getElementById("tr"+i.toString()).appendChild(thnum);
    //    document.getElementById("tr"+i.toString()).appendChild(thmatch);
    //    document.getElementById("tr"+i.toString()).appendChild(thpage);
    //    document.getElementById("tr"+i.toString()).appendChild(thmatchesnum); 
    //}
    document.getElementById('searchtablebody').innerHTML="<tr><th>№</th><th>Match</th><th>Pages</th><th>Matches</th></tr>"
    var i =0;
    for (const [key, value] of Object.entries(result['tablematch'])) {
        //console.log(key, value);
        const tr = document.createElement("tr");
        const thnum = document.createElement("th");
        const thmatch = document.createElement("th");
        const thpage = document.createElement("th");
        const thmatchesnum = document.createElement("th");
        thnum.innerHTML=i+1;
        thmatch.innerHTML=`<span class="pagelink" onclick="search('`+key+`')">`+key+`</span>`;
        //onclick="search('+key+')"
        
        //console.log(linkpages(value[0]).toString());
        thpage.innerHTML= linkpages(value[0]).toString();
        
        //value[0];
        thmatchesnum.innerHTML=value[1];
        tr.setAttribute('id','tr'+i.toString());
        document.getElementById("searchtablebody").appendChild(tr); 
        document.getElementById("tr"+i.toString()).appendChild(thnum);
        document.getElementById("tr"+i.toString()).appendChild(thmatch);
        document.getElementById("tr"+i.toString()).appendChild(thpage);
        document.getElementById("tr"+i.toString()).appendChild(thmatchesnum); 
        i=i+1
    }
    
        
    //document.getElementById("searchresblock").style.display="block";
    //const tr = document.createElement("tr");
    //const thnum = document.createElement("th");
    //const thmatch = document.createElement("th");
    //const thpage = document.createElement("th");
    //const thmatchesnum = document.createElement("th");
    //thnum.innerHTML="1";
    //thmatch.innerHTML="Iporto";
    //thpage.innerHTML="4";
    //thmatchesnum.innerHTML="3";
    //tr.setAttribute('id','tr1');
    //document.getElementById("searchtablebody").appendChild(tr); 
    //document.getElementById("tr1").appendChild(thnum);
    //document.getElementById("tr1").appendChild(thmatch);
    //document.getElementById("tr1").appendChild(thpage);
    //document.getElementById("tr1").appendChild(thmatchesnum); 
 
 
 
    
    }}





function searchbtn(){
  //var prolonged;
  //document.getElementById("searchresblock").style.display="block";
  var inputfield = document.getElementById("searchinput");
  var server_data = [
  {"input": inputfield.value}
];

$.ajax({
  type: "POST",
  url: "/process_qtc",
  data: JSON.stringify(server_data),
  contentType: "application/json",
  dataType: 'json',
  success: function(result) {
    console.log("Result:");
    console.log(result);
    placeintable(result);
  } 
});

}
</script>
  </head>

  <body tabindex="1">


  	<div id="topMenu">
  	    
  		<input type="Text" id="searchinput" name="searchtext" placeholder="Fuzzy search.."> 
  		<button class="searchbtn" id="searchbtn" onclick="searchbtn()">Fuzzy search</button><button class="searchbtn" onclick="document.getElementById('openFile').click()">Upload <i class="fas fa-upload"></i></button>
  		<br>
  		<!-- <div id="infobox" >
  		<i id="infoicon" class="fas fa-info-circle" onclick="infobtn();" > </i><span onclick="infobtn();" id="btnlabeltext"
  		>what does Fuzzy search mean?</span></div> -->
  		<div id="tableofmathes">
<!--
  		<div id="header"><span>№</span><span>Match</span><span>Page</span><span>Matches on page</span></div>
  		<div id="content1"><span>1</span><span>Importont</span><span>3</span><span>2</span></div>
 -->
 <div id="searchresblock" style="display:none;">
<table id="searchtable" >
<tbody id="searchtablebody">
  <tr>
    <th>№</th>
    <th>Match</th>
    <th>Pages</th>
    <th>Matches</th>
  </tr>
 </tbody>
  <!--<tr>
    <td>1</td>
    <td class="pagelink" onclick="search();">Maria Anders</td>
    <td><span class="pagelink" >11</span>, <span class="pagelink">2</span></td>
    <td>2</td>
  </tr>
  <tr>
    <td>2</td>
    <td class="pagelink">Francisco Chang</td>
    <td><span class="pagelink" >2</span>, <span class="pagelink">5</span></td>
    <td>2</td>

  </tr>
  <tr>
    <td>3</td>
    <td class="pagelink">Roland Mendel</td>
    <td><span class="pagelink" >6</span>, <span class="pagelink">7</span>, <span class="pagelink">8</span></td>
    <td>3</td>
  </tr>
  <tr>
    <td>4</td>
    <td class="pagelink">Helen Bennett</td>
    <td><span class="pagelink" >1</span>, <span class="pagelink">6</span></td>
    <td>2</td>
  </tr>
  <tr>
    <td>5</td>
    <td class="pagelink">Yoshi Tannamuri</td>
    <td><span class="pagelink" >3</span></td>
    <td>1</td>
  </tr>
  <tr>
    <td>6</td>
    <td class="pagelink">Giovanni Rovelli</td>
    <td><span class="pagelink" >13</span></td>
    <td>1</td>
  </tr>-->
</table>
<div id="searchall">
<button id="Previousbtn"class="searchbtn" >Find previous<<</button> <button id="Nextbtn" class="searchbtn">Find next >></button>
</div>
</div>
  		</div>
<div id="infobox" >
  		<i id="infoicon" class="fas fa-info-circle" onclick="infobtn();" > </i><span onclick="infobtn();" id="btnlabeltext"
  		>what does Fuzzy search mean?</span></div>
  		<div id="textaboutfuzzysearch" style="display: none;"><br>
    sdhfjkusdfkj hksdfjsd kjfdsh
    <br>
    sdhfjkusdfkj hksdfjsd kjfdsh
    <br>
    sdhfjkusdfkj hksdfjsd kjfdsh
    <br>
    sdhfjkusdfkj hksdfjsd kjfdsh
    <br></div>
  		<!-- <button style="display: block; margin-top: 1%;">what does Fuzzy search mean?</button> -->
<!--     sdhfjkusdfkj hksdfjsd kjfdsh
    <br>
    sdhfjkusdfkj hksdfjsd kjfdsh
    <br>
    sdhfjkusdfkj hksdfjsd kjfdsh
    <br>
    sdhfjkusdfkj hksdfjsd kjfdsh
    <br>
    sdhfjkusdfkj hksdfjsd kjfdsh
    <br> -->
    </div>
    <div id="outerContainer">

      <div id="sidebarContainer">
        <div id="toolbarSidebar">
          <div id="toolbarSidebarLeft">
            <div class="splitToolbarButton toggled">
              <button id="viewThumbnail" class="toolbarButton toggled" title="Show Thumbnails" tabindex="2" data-l10n-id="thumbs">
                 <span data-l10n-id="thumbs_label">Thumbnails</span>
              </button>
              <button id="viewOutline" class="toolbarButton" title="Show Document Outline (double-click to expand/collapse all items)" tabindex="3" data-l10n-id="document_outline">
                 <span data-l10n-id="document_outline_label">Document Outline</span>
              </button>
              <button id="viewAttachments" class="toolbarButton" title="Show Attachments" tabindex="4" data-l10n-id="attachments">
                 <span data-l10n-id="attachments_label">Attachments</span>
              </button>
              <button id="viewLayers" class="toolbarButton" title="Show Layers (double-click to reset all layers to the default state)" tabindex="5" data-l10n-id="layers">
                 <span data-l10n-id="layers_label">Layers</span>
              </button>
            </div>
          </div>

          <div id="toolbarSidebarRight">
            <div id="outlineOptionsContainer" class="hidden">
              <div class="verticalToolbarSeparator"></div>

              <button id="currentOutlineItem" class="toolbarButton" disabled="disabled" title="Find Current Outline Item" tabindex="6" data-l10n-id="current_outline_item">
                <span data-l10n-id="current_outline_item_label">Current Outline Item</span>
              </button>
            </div>
          </div>
        </div>
        <div id="sidebarContent">
          <div id="thumbnailView">
          </div>
          <div id="outlineView" class="hidden">
          </div>
          <div id="attachmentsView" class="hidden">
          </div>
          <div id="layersView" class="hidden">
          </div>
        </div>
        <div id="sidebarResizer"></div>
      </div>  <!-- sidebarContainer -->

      <div id="mainContainer">
        <div class="findbar hidden doorHanger" id="findbar">
          <div id="findbarInputContainer">
            <input id="findInput" class="toolbarField" title="Find" placeholder="Find in document…" tabindex="91" data-l10n-id="find_input">
            <div class="splitToolbarButton">
              <button id="findPrevious" class="toolbarButton findPrevious" title="Find the previous occurrence of the phrase" tabindex="92" data-l10n-id="find_previous">
                <span data-l10n-id="find_previous_label">Previous</span>
              </button>
              <div class="splitToolbarButtonSeparator"></div>
              <button id="findNext" class="toolbarButton findNext" title="Find the next occurrence of the phrase" tabindex="93" data-l10n-id="find_next">
                <span data-l10n-id="find_next_label">Next</span>
              </button>
            </div>
          </div>

          <div id="findbarOptionsOneContainer">
            <input type="checkbox" id="findHighlightAll" class="toolbarField" tabindex="94">
            <label for="findHighlightAll" class="toolbarLabel" data-l10n-id="find_highlight">Highlight all</label>
            <input type="checkbox" id="findMatchCase" class="toolbarField" tabindex="95">
            <label for="findMatchCase" class="toolbarLabel" data-l10n-id="find_match_case_label">Match case</label>
          </div>
          <div id="findbarOptionsTwoContainer">
            <input type="checkbox" id="findEntireWord" class="toolbarField" tabindex="96">
            <label for="findEntireWord" class="toolbarLabel" data-l10n-id="find_entire_word_label">Whole words</label>
            <span id="findResultsCount" class="toolbarLabel hidden"></span>
          </div>

          <div id="findbarMessageContainer">
            <span id="findMsg" class="toolbarLabel"></span>
          </div>
        </div>  <!-- findbar -->

        <div id="secondaryToolbar" class="secondaryToolbar hidden doorHangerRight">
          <div id="secondaryToolbarButtonContainer">
            <button id="secondaryPresentationMode" class="secondaryToolbarButton presentationMode visibleLargeView" title="Switch to Presentation Mode" tabindex="51" data-l10n-id="presentation_mode">
              <span data-l10n-id="presentation_mode_label">Presentation Mode</span>
            </button>

            <button id="secondaryOpenFile" class="secondaryToolbarButton openFile visibleLargeView" title="Open File" tabindex="52" data-l10n-id="open_file">
              <span data-l10n-id="open_file_label">Open</span>
            </button>

            <button id="secondaryPrint" class="secondaryToolbarButton print visibleMediumView" title="Print" tabindex="53" data-l10n-id="print">
              <span data-l10n-id="print_label">Print</span>
            </button>

            <button id="secondaryDownload" class="secondaryToolbarButton download visibleMediumView" title="Download" tabindex="54" data-l10n-id="download">
              <span data-l10n-id="download_label">Download</span>
            </button>

            <a href="#" id="secondaryViewBookmark" class="secondaryToolbarButton bookmark visibleSmallView" title="Current view (copy or open in new window)" tabindex="55" data-l10n-id="bookmark">
              <span data-l10n-id="bookmark_label">Current View</span>
            </a>

            <div class="horizontalToolbarSeparator visibleLargeView"></div>

            <button id="firstPage" class="secondaryToolbarButton firstPage" title="Go to First Page" tabindex="56" data-l10n-id="first_page">
              <span data-l10n-id="first_page_label">Go to First Page</span>
            </button>
            <button id="lastPage" class="secondaryToolbarButton lastPage" title="Go to Last Page" tabindex="57" data-l10n-id="last_page">
              <span data-l10n-id="last_page_label">Go to Last Page</span>
            </button>

            <div class="horizontalToolbarSeparator"></div>

            <button id="pageRotateCw" class="secondaryToolbarButton rotateCw" title="Rotate Clockwise" tabindex="58" data-l10n-id="page_rotate_cw">
              <span data-l10n-id="page_rotate_cw_label">Rotate Clockwise</span>
            </button>
            <button id="pageRotateCcw" class="secondaryToolbarButton rotateCcw" title="Rotate Counterclockwise" tabindex="59" data-l10n-id="page_rotate_ccw">
              <span data-l10n-id="page_rotate_ccw_label">Rotate Counterclockwise</span>
            </button>

            <div class="horizontalToolbarSeparator"></div>

            <button id="cursorSelectTool" class="secondaryToolbarButton selectTool toggled" title="Enable Text Selection Tool" tabindex="60" data-l10n-id="cursor_text_select_tool">
              <span data-l10n-id="cursor_text_select_tool_label">Text Selection Tool</span>
            </button>
            <button id="cursorHandTool" class="secondaryToolbarButton handTool" title="Enable Hand Tool" tabindex="61" data-l10n-id="cursor_hand_tool">
              <span data-l10n-id="cursor_hand_tool_label">Hand Tool</span>
            </button>

            <div class="horizontalToolbarSeparator"></div>

            <button id="scrollPage" class="secondaryToolbarButton scrollPage" title="Use Page Scrolling" tabindex="62" data-l10n-id="scroll_page">
              <span data-l10n-id="scroll_page_label">Page Scrolling</span>
            </button>
            <button id="scrollVertical" class="secondaryToolbarButton scrollVertical toggled" title="Use Vertical Scrolling" tabindex="63" data-l10n-id="scroll_vertical">
              <span data-l10n-id="scroll_vertical_label">Vertical Scrolling</span>
            </button>
            <button id="scrollHorizontal" class="secondaryToolbarButton scrollHorizontal" title="Use Horizontal Scrolling" tabindex="64" data-l10n-id="scroll_horizontal">
              <span data-l10n-id="scroll_horizontal_label">Horizontal Scrolling</span>
            </button>
            <button id="scrollWrapped" class="secondaryToolbarButton scrollWrapped" title="Use Wrapped Scrolling" tabindex="65" data-l10n-id="scroll_wrapped">
              <span data-l10n-id="scroll_wrapped_label">Wrapped Scrolling</span>
            </button>

            <div class="horizontalToolbarSeparator"></div>

            <button id="spreadNone" class="secondaryToolbarButton spreadNone toggled" title="Do not join page spreads" tabindex="66" data-l10n-id="spread_none">
              <span data-l10n-id="spread_none_label">No Spreads</span>
            </button>
            <button id="spreadOdd" class="secondaryToolbarButton spreadOdd" title="Join page spreads starting with odd-numbered pages" tabindex="67" data-l10n-id="spread_odd">
              <span data-l10n-id="spread_odd_label">Odd Spreads</span>
            </button>
            <button id="spreadEven" class="secondaryToolbarButton spreadEven" title="Join page spreads starting with even-numbered pages" tabindex="68" data-l10n-id="spread_even">
              <span data-l10n-id="spread_even_label">Even Spreads</span>
            </button>

            <div class="horizontalToolbarSeparator"></div>

            <button id="documentProperties" class="secondaryToolbarButton documentProperties" title="Document Properties…" tabindex="69" data-l10n-id="document_properties">
              <span data-l10n-id="document_properties_label">Document Properties…</span>
            </button>
          </div>
        </div>  <!-- secondaryToolbar -->

        <div class="toolbar">
          <div id="toolbarContainer">
            <div id="toolbarViewer">
              <div id="toolbarViewerLeft">
                <button id="sidebarToggle" class="toolbarButton" title="Toggle Sidebar" tabindex="11" data-l10n-id="toggle_sidebar" aria-expanded="false" aria-controls="sidebarContainer">
                  <span data-l10n-id="toggle_sidebar_label">Toggle Sidebar</span>
                </button>
                <div class="toolbarButtonSpacer"></div>
                <button id="viewFind" class="toolbarButton" title="Find in Document" tabindex="12" data-l10n-id="findbar" aria-expanded="false" aria-controls="findbar">
                  <span data-l10n-id="findbar_label">Find</span>
                </button>
                <div class="splitToolbarButton hiddenSmallView">
                  <button class="toolbarButton pageUp" title="Previous Page" id="previous" tabindex="13" data-l10n-id="previous">
                    <span data-l10n-id="previous_label">Previous</span>
                  </button>
                  <div class="splitToolbarButtonSeparator"></div>
                  <button class="toolbarButton pageDown" title="Next Page" id="next" tabindex="14" data-l10n-id="next">
                    <span data-l10n-id="next_label">Next</span>
                  </button>
                </div>
                <input type="number" id="pageNumber" class="toolbarField pageNumber" title="Page" value="1" size="4" min="1" tabindex="15" data-l10n-id="page" autocomplete="off">
                <span id="numPages" class="toolbarLabel"></span>
              </div>
              <div id="toolbarViewerRight">
                <button id="presentationMode" class="toolbarButton presentationMode hiddenLargeView" title="Switch to Presentation Mode" tabindex="31" data-l10n-id="presentation_mode">
                  <span data-l10n-id="presentation_mode_label">Presentation Mode</span>
                </button>

                <button id="openFile" class="toolbarButton openFile hiddenLargeView" title="Open File" tabindex="32" data-l10n-id="open_file">
                  <span data-l10n-id="open_file_label">Open</span>
                </button>

                <button id="print" class="toolbarButton print hiddenMediumView" title="Print" tabindex="33" data-l10n-id="print">
                  <span data-l10n-id="print_label">Print</span>
                </button>

                <button id="download" class="toolbarButton download hiddenMediumView" title="Download" tabindex="34" data-l10n-id="download">
                  <span data-l10n-id="download_label">Download</span>
                </button>
                <a href="#" id="viewBookmark" class="toolbarButton bookmark hiddenSmallView" title="Current view (copy or open in new window)" tabindex="35" data-l10n-id="bookmark">
                  <span data-l10n-id="bookmark_label">Current View</span>
                </a>

                <div class="verticalToolbarSeparator hiddenSmallView"></div>

                <button id="secondaryToolbarToggle" class="toolbarButton" title="Tools" tabindex="36" data-l10n-id="tools" aria-expanded="false" aria-controls="secondaryToolbar">
                  <span data-l10n-id="tools_label">Tools</span>
                </button>
              </div>
              <div id="toolbarViewerMiddle">
                <div class="splitToolbarButton">
                  <button id="zoomOut" class="toolbarButton zoomOut" title="Zoom Out" tabindex="21" data-l10n-id="zoom_out">
                    <span data-l10n-id="zoom_out_label">Zoom Out</span>
                  </button>
                  <div class="splitToolbarButtonSeparator"></div>
                  <button id="zoomIn" class="toolbarButton zoomIn" title="Zoom In" tabindex="22" data-l10n-id="zoom_in">
                    <span data-l10n-id="zoom_in_label">Zoom In</span>
                   </button>
                </div>
                <span id="scaleSelectContainer" class="dropdownToolbarButton">
                  <select id="scaleSelect" title="Zoom" tabindex="23" data-l10n-id="zoom">
                    <option id="pageAutoOption" title="" value="auto" selected="selected" data-l10n-id="page_scale_auto">Automatic Zoom</option>
                    <option id="pageActualOption" title="" value="page-actual" data-l10n-id="page_scale_actual">Actual Size</option>
                    <option id="pageFitOption" title="" value="page-fit" data-l10n-id="page_scale_fit">Page Fit</option>
                    <option id="pageWidthOption" title="" value="page-width" data-l10n-id="page_scale_width">Page Width</option>
                    <option id="customScaleOption" title="" value="custom" disabled="disabled" hidden="true"></option>
                    <option title="" value="0.5" data-l10n-id="page_scale_percent" data-l10n-args='{ "scale": 50 }'>50%</option>
                    <option title="" value="0.75" data-l10n-id="page_scale_percent" data-l10n-args='{ "scale": 75 }'>75%</option>
                    <option title="" value="1" data-l10n-id="page_scale_percent" data-l10n-args='{ "scale": 100 }'>100%</option>
                    <option title="" value="1.25" data-l10n-id="page_scale_percent" data-l10n-args='{ "scale": 125 }'>125%</option>
                    <option title="" value="1.5" data-l10n-id="page_scale_percent" data-l10n-args='{ "scale": 150 }'>150%</option>
                    <option title="" value="2" data-l10n-id="page_scale_percent" data-l10n-args='{ "scale": 200 }'>200%</option>
                    <option title="" value="3" data-l10n-id="page_scale_percent" data-l10n-args='{ "scale": 300 }'>300%</option>
                    <option title="" value="4" data-l10n-id="page_scale_percent" data-l10n-args='{ "scale": 400 }'>400%</option>
                  </select>
                </span>
              </div>
            </div>
            <div id="loadingBar">
              <div class="progress">
                <div class="glimmer">
                </div>
              </div>
            </div>
          </div>
        </div>

        <div id="viewerContainer" tabindex="0">
          <div id="viewer" class="pdfViewer"></div>
        </div>

        <div id="errorWrapper" hidden='true'>
          <div id="errorMessageLeft">
            <span id="errorMessage"></span>
            <button id="errorShowMore" data-l10n-id="error_more_info">
              More Information
            </button>
            <button id="errorShowLess" data-l10n-id="error_less_info" hidden='true'>
              Less Information
            </button>
          </div>
          <div id="errorMessageRight">
            <button id="errorClose" data-l10n-id="error_close">
              Close
            </button>
          </div>
          <div class="clearBoth"></div>
          <textarea id="errorMoreInfo" hidden='true' readonly="readonly"></textarea>
        </div>
      </div> <!-- mainContainer -->

      <div id="overlayContainer" class="hidden">
        <div id="passwordOverlay" class="container hidden">
          <div class="dialog">
            <div class="row">
              <p id="passwordText" data-l10n-id="password_label">Enter the password to open this PDF file:</p>
            </div>
            <div class="row">
              <input type="password" id="password" class="toolbarField">
            </div>
            <div class="buttonRow">
              <button id="passwordCancel" class="overlayButton"><span data-l10n-id="password_cancel">Cancel</span></button>
              <button id="passwordSubmit" class="overlayButton"><span data-l10n-id="password_ok">OK</span></button>
            </div>
          </div>
        </div>
        <div id="documentPropertiesOverlay" class="container hidden">
          <div class="dialog">
            <div class="row">
              <span data-l10n-id="document_properties_file_name">File name:</span> <p id="fileNameField">-</p>
            </div>
            <div class="row">
              <span data-l10n-id="document_properties_file_size">File size:</span> <p id="fileSizeField">-</p>
            </div>
            <div class="separator"></div>
            <div class="row">
              <span data-l10n-id="document_properties_title">Title:</span> <p id="titleField">-</p>
            </div>
            <div class="row">
              <span data-l10n-id="document_properties_author">Author:</span> <p id="authorField">-</p>
            </div>
            <div class="row">
              <span data-l10n-id="document_properties_subject">Subject:</span> <p id="subjectField">-</p>
            </div>
            <div class="row">
              <span data-l10n-id="document_properties_keywords">Keywords:</span> <p id="keywordsField">-</p>
            </div>
            <div class="row">
              <span data-l10n-id="document_properties_creation_date">Creation Date:</span> <p id="creationDateField">-</p>
            </div>
            <div class="row">
              <span data-l10n-id="document_properties_modification_date">Modification Date:</span> <p id="modificationDateField">-</p>
            </div>
            <div class="row">
              <span data-l10n-id="document_properties_creator">Creator:</span> <p id="creatorField">-</p>
            </div>
            <div class="separator"></div>
            <div class="row">
              <span data-l10n-id="document_properties_producer">PDF Producer:</span> <p id="producerField">-</p>
            </div>
            <div class="row">
              <span data-l10n-id="document_properties_version">PDF Version:</span> <p id="versionField">-</p>
            </div>
            <div class="row">
              <span data-l10n-id="document_properties_page_count">Page Count:</span> <p id="pageCountField">-</p>
            </div>
            <div class="row">
              <span data-l10n-id="document_properties_page_size">Page Size:</span> <p id="pageSizeField">-</p>
            </div>
            <div class="separator"></div>
            <div class="row">
              <span data-l10n-id="document_properties_linearized">Fast Web View:</span> <p id="linearizedField">-</p>
            </div>
            <div class="buttonRow">
              <button id="documentPropertiesClose" class="overlayButton"><span data-l10n-id="document_properties_close">Close</span></button>
            </div>
          </div>
        </div>
        <div id="printServiceOverlay" class="container hidden">
          <div class="dialog">
            <div class="row">
              <span data-l10n-id="print_progress_message">Preparing document for printing…</span>
            </div>
            <div class="row">
              <progress value="0" max="100"></progress>
              <span data-l10n-id="print_progress_percent" data-l10n-args='{ "progress": 0 }' class="relative-progress">0%</span>
            </div>
            <div class="buttonRow">
              <button id="printCancel" class="overlayButton"><span data-l10n-id="print_progress_close">Cancel</span></button>
            </div>
          </div>
        </div>
      </div>  <!-- overlayContainer -->

    </div> <!-- outerContainer -->
    <div id="printContainer"></div>
  </body>
</html>
'''
app.run()