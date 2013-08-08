
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

from app import app
import os
from flask import Flask, render_template, send_from_directory, send_file, request, url_for, jsonify, redirect, Request, g

from cStringIO import StringIO
from werkzeug import secure_filename

os.environ[ 'MPLCONFIGDIR' ] = '/tmp/'

import matplotlib
matplotlib.use('Agg')
#import numpy
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as numpy

from PIL import Image
import gc


UPLOAD_FOLDER = os.path.join(app.root_path, 'uploads')
NDVI_FOLDER = os.path.join(app.root_path, 'ndvi')

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif','PNG','JPEG','JPG'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['NDVI_FOLDER'] = NDVI_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16*1024*1024
app.debug = True
app.static_folder = 'static'
app.static_url_path = ''

#@app.errorhandler(413)
#def file_to_big(e):
#    return render_template('tooBig.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.static_folder, request.path[1:])

def nir(imageInPath,imageOutPath):
    img=Image.open(imageInPath)
    imgR, imgG, imgB = img.split() #get channels
    arrR = numpy.asarray(imgR).astype('float64')

    arr_nir=arrR

    img_w,img_h=img.size

    dpi=600. #need this to be floating point!
    fig_w=img_w/dpi
    fig_h=img_h/dpi

    fig=plt.figure(figsize=(fig_w,fig_h),dpi=dpi)

    fig.set_frameon(False)

    ax_rect = [0.0, #left
           0.0, #bottom
           1.0, #width
           1.0] #height
    ax = fig.add_axes(ax_rect)
    ax.yaxis.set_ticklabels([])
    ax.xaxis.set_ticklabels([])   
    ax.set_axis_off()
    ax.axes.get_yaxis().set_visible(False)
    ax.patch.set_alpha(0.0)

    axes_img = ax.imshow(arr_nir,
              cmap=plt.cm.gist_gray,
              aspect = 'equal',
              interpolation="nearest"
             )

    fig.savefig(imageOutPath, 
            dpi=dpi,
            bbox_inches='tight',
            pad_inches=0.0, 
           )

    #plt.show()  #show the plot after saving
    fig.clf()
    plt.close()
    gc.collect()

def only_blue(imageInPath,imageOutPath):
    img=Image.open(imageInPath)
    imgR, imgG, imgB = img.split() #get channels
    arrB = numpy.asarray(imgB).astype('float64')

    arr_only_blue=arrB

    img_w,img_h=img.size

    dpi=600. #need this to be floating point!
    fig_w=img_w/dpi
    fig_h=img_h/dpi

    fig=plt.figure(figsize=(fig_w,fig_h),dpi=dpi)

    fig.set_frameon(False)

    ax_rect = [0.0, #left
           0.0, #bottom
           1.0, #width
           1.0] #height
    ax = fig.add_axes(ax_rect)
    ax.yaxis.set_ticklabels([])
    ax.xaxis.set_ticklabels([])   
    ax.set_axis_off()
    ax.axes.get_yaxis().set_visible(False)
    ax.patch.set_alpha(0.0)

    axes_img = ax.imshow(arr_only_blue,
              cmap=plt.cm.gist_gray,
              aspect = 'equal',
              interpolation="nearest"
             )

    fig.savefig(imageOutPath, 
            dpi=dpi,
            bbox_inches='tight',
            pad_inches=0.0, 
           )

    #plt.show()  #show the plot after saving
    fig.clf()
    plt.close()
    gc.collect()




def ndvi(imageInPath,imageOutPath):
    img=Image.open(imageInPath)
    imgR, imgG, imgB = img.split() #get channels
    arrR = numpy.asarray(imgR).astype('float64')
    arrB = numpy.asarray(imgB).astype('float64')
    
    num=arrR - arrB
    num=(arrR - arrB)
    denom=(arrR + arrB)
    arr_ndvi=num/denom

    vmin=-1.
    vmax = 1.

    img_w,img_h=img.size

    dpi=600. #need this to be floating point!
    fig_w=img_w/dpi
    fig_h=img_h/dpi

    fig=plt.figure(figsize=(fig_w,fig_h),dpi=dpi,linewidth=0.3)

    fig.set_frameon(False)

    ax_rect = [0.0, #left
           0.0, #bottom
           1.0, #width
           1.0] #height
    ax = fig.add_axes(ax_rect)
    ax.yaxis.set_ticklabels([])
    ax.xaxis.set_ticklabels([])   
    ax.set_axis_off()
    ax.axes.get_yaxis().set_visible(False)
    ax.patch.set_alpha(0.0)

    cdict = {
    'red'  :  ((0.00, 0.00, 0.00), 
               (0.20, 0.00, 0.00),
               (0.50, 0.00, .00),
               (0.70, 1.00, 1.00),
               (1.00, 1.00, 1.00)),
    'green':  ((0.00, 0.00, 0.00), 
               (0.20, 0.00, 0.00),
               (0.50, 1.00,.50),
               (0.70, 1.00, 1.00),
               (1.00, 0.00, 0.00)),
    'blue' :  ((0.00, 0.00, 0.00), 
               (0.20, 1.00, 1.00),
    #           (0.40, 0.00, 0.00),
               (0.50, 1.00, 0.00),
               (0.70, 0.00, 0.00), 
               (1.00, 0.00, 0.00)),
    }


    fastie_cmap = matplotlib.colors.LinearSegmentedColormap('my_colormap',cdict,256)


    axes_img = ax.imshow(arr_ndvi,
#              cmap=plt.cm.spectral, 
              cmap=fastie_cmap,
              aspect = 'equal',
              interpolation="nearest",
              vmin=-1.0,
              vmax=1.0
             )

    # Add colorbar 
    #make an axis for colorbar
    cax = fig.add_axes([0.8,0.05,0.05,0.85]) #left, bottom, width, height
    cbar = fig.colorbar(axes_img, cax=cax)  #this resizes the axis
    cbar.ax.tick_params(labelsize=2) #this changes the font size on the axis

    fig.savefig(imageOutPath, 
            dpi=dpi,
            bbox_inches='tight',
            pad_inches=0.0, 
           )

    #plt.show()  #show the plot after saving
    fig.clf()
    plt.close()
    gc.collect()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method=='POST':
        file=request.files['file']
        if file and allowed_file(file.filename):
            filename=secure_filename(file.filename)
            uploadFilePath=os.path.join(app.config['UPLOAD_FOLDER'],filename)
            file.save(uploadFilePath)
            ndviFilePath=os.path.join(app.config['UPLOAD_FOLDER'],'ndvi_'+filename)
            nirFilePath=os.path.join(app.config['UPLOAD_FOLDER'],'nir_'+filename)
            blueFilePath=os.path.join(app.config['UPLOAD_FOLDER'],'blue_'+filename)
            ndvi(uploadFilePath,ndviFilePath)
            nir(uploadFilePath,nirFilePath)
            only_blue(uploadFilePath,blueFilePath)
            return redirect(url_for('uploaded_file',filename=filename)) 
    return render_template('index.html')

@app.route('/dragdrop')
def dragdrop():
    return render_template('dragdrop.html')

@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(UPLOAD_FOLDER,filename)


@app.route('/show/<filename>')
def uploaded_file(filename):
    uploadFilePath=os.path.join(app.config['UPLOAD_FOLDER'],filename)
    ndviFilePath=os.path.join(app.config['NDVI_FOLDER'],filename)  
    return render_template('render.html',filename='/uploads/'+filename, ndviFilename='/uploads/'+'ndvi_'+filename, nirFilename='/uploads/'+'nir_'+filename, blueFilename='/uploads/'+'blue_'+filename)

# testing connection between Flask and jquery functions ...
@app.route('/jqueryTest')
def jqueryTest():
    return render_template('jqueryTest.html')

@app.route('/_add_numbers')
def add_numbers():
    """Add two numbers server side, ridiculous but well..."""
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)

# testing clicking somewhere on an image
@app.route('/clickTest')
def clickTest():
    return render_template('clickcoord.html')


