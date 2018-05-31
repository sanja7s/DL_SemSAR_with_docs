import os
import gdal
import osr

def get_extent(dataset):

    cols = dataset.RasterXSize
    rows = dataset.RasterYSize
    transform = dataset.GetGeoTransform()
    minx = transform[0]
    maxx = transform[0] + cols * transform[1] + rows * transform[2]

    miny = transform[3] + cols * transform[4] + rows * transform[5]
    maxy = transform[3]

    return {
            "minX": str(minx), "maxX": str(maxx),
            "minY": str(miny), "maxY": str(maxy),
            "cols": str(cols), "rows": str(rows)
            }


def take_out_test_pred_and_gt_data(models_DIR, model_name, out_dir):
    # we also take out the validation dataset from the training

    data_dir = os.path.join(models_DIR, model_name)
    test_images_dir = os.path.join(data_dir, 'test')

    res_images_dir = os.path.join(models_DIR, 'TEST7s')

    files = os.listdir(res_images_dir)
    driver = gdal.GetDriverByName('GTiff')

    for f in sorted(files):

        if not f.endswith('.png'):
            continue

        test_img_name = f.replace('_pred',"").replace('_gt',"").replace('.png',".tif")
        test_img_path = os.path.join(test_images_dir, test_img_name)     
        output_img_path = os.path.join(out_dir, 'orig', test_img_name)

        def save_test_image_and_get_georef_info(test_img_path, output_img_path):

            test_img = gdal.Open(test_img_path)

            transform = test_img.GetGeoTransform()
            xOrigin = transform[0]
            yOrigin = transform[3]
            pixelWidth = transform[1]
            pixelHeight = -transform[5]
            new_cols = 1024
            new_rows = 1024

            srcbands = []
            for band in range( test_img.RasterCount ):
                band += 1
                #print ("[ GETTING BAND ]: ", band)
                srcband = test_img.GetRasterBand(band)
                if srcband is None:
                    continue
                else:
                    srcbands.append(srcband)

            # hard-coded crop; can be changed to check what is the size of predicted file
            data = []
            for srcband in srcbands:
                data.append(srcband.ReadAsArray(0, 0, new_cols, new_rows))

            dst_ds = driver.Create(output_img_path,
                                   new_cols,
                                   new_rows,
                                   test_img.RasterCount,
                                   gdal.GDT_Float32)

            #writting output raster
            for band in range( test_img.RasterCount ):
                band += 1
                dst_ds.GetRasterBand(band).SetNoDataValue(0)
                dst_ds.GetRasterBand(band).WriteArray( data[band-1] )

            #setting extension of output raster
            # top left x, w-e pixel resolution, rotation, top left y, rotation, n-s pixel resolution
            dst_ds.SetGeoTransform(transform)
            wkt = test_img.GetProjection()

            # setting spatial reference of output raster
            srs = osr.SpatialReference()
            srs.ImportFromWkt(wkt)
            dst_ds.SetProjection( srs.ExportToWkt() )


            #Close output raster dataset
            dst_ds = None

            return transform, srs
     

        ###########################################################################
        
        src_img_path = os.path.join(res_images_dir, f)

        if f.endswith('gt.png'):
            dest_img_path = os.path.join(out_dir, 'gt', f)
            transform, srs = save_test_image_and_get_georef_info(test_img_path, output_img_path)
        elif f.endswith('pred.png'):
            dest_img_path = os.path.join(out_dir, 'pred', f)

        img = gdal.Open(src_img_path)
        # Open destination dataset
        dst_img = driver.CreateCopy(dest_img_path, img, 0)

        dst_img.SetGeoTransform(transform)
        #wkt = test_img.GetProjection()

        # setting spatial reference of output raster
        dst_img.SetProjection( srs.ExportToWkt() )

        #Close output raster dataset
        dst_img = None

        #return





current_dir = os.path.abspath(os.path.dirname(__file__))
print ('project', current_dir)

models_DIR = os.path.join(current_dir, '../../data/DL_models/Semantic-Segmentation-Suite/')
out_dir = os.path.join(current_dir, '../../data/DL_output/')

model_name='Corine-Sentinel-DEM'

take_out_test_pred_and_gt_data(models_DIR, model_name, out_dir)