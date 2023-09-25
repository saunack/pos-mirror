package com.posmirror.posmirror;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;

import android.content.pm.PackageManager;
import android.os.Bundle;
import android.util.Log;

import org.opencv.android.CameraActivity;
import org.opencv.android.CameraBridgeViewBase;
import org.opencv.android.OpenCVLoader;
import org.opencv.core.Mat;
import org.opencv.core.MatOfPoint;
import org.opencv.core.Rect;
import org.opencv.core.Scalar;
import org.opencv.core.Size;
import org.opencv.imgproc.Imgproc;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.Comparator;
import java.util.Iterator;
import java.util.List;
import java.util.ListIterator;
import java.util.NoSuchElementException;

public class MainActivity extends CameraActivity {
    CameraBridgeViewBase cameraBridgeViewBase;

    Comparator<MatOfPoint> desc_comp = new Comparator<MatOfPoint>() {
        @Override
        public int compare(MatOfPoint t1, MatOfPoint t2) {
            if (Imgproc.contourArea(t1) > Imgproc.contourArea(t2))
                return -1;
            else if (Imgproc.contourArea(t1) == Imgproc.contourArea(t2))
                return 0;
            else
                return 1;
        }
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        getPermission();

        cameraBridgeViewBase = findViewById(R.id.cameraView);

        cameraBridgeViewBase.setCvCameraViewListener(new CameraBridgeViewBase.CvCameraViewListener2() {
            @Override
            public void onCameraViewStarted(int width, int height) {
                // intiailze all matrices
            }

            @Override
            public void onCameraViewStopped() {
                //rleease resource
            }

            @Override
            public Mat onCameraFrame(CameraBridgeViewBase.CvCameraViewFrame inputFrame) {
                Mat frame = inputFrame.rgba();
                Mat gray = inputFrame.gray();
//                Imgproc.Canny(gray, gray, 80, 100);

                Mat blurred_gray_image = new Mat();
                Imgproc.blur(gray, blurred_gray_image, new Size(21, 21));
                Mat thresholded_blurry_image = new Mat();
                Imgproc.threshold(gray, thresholded_blurry_image, 165,255,Imgproc.THRESH_BINARY);
//                return thresholded_blurry_image;
                List<MatOfPoint> contours = new ArrayList<MatOfPoint>();
                Mat hierarchy = new Mat();
                Imgproc.findContours(thresholded_blurry_image, contours, hierarchy, Imgproc.RETR_TREE, Imgproc.CHAIN_APPROX_SIMPLE);

                Collections.sort(contours, desc_comp); // max directly
//                double x = Imgproc.contourArea(contours.get(0));
//                Log.d("opencv",String.valueOf(x));
//                double y = Imgproc.contourArea(contours.get(2));
//                Log.d("opencv",String.valueOf(y));
//                ArrayList<MatOfPoint> page = new ArrayList<>();
//                for(int i=0;i<5;i++){
//                    page.set(i, contours.get(i));
//                }
//                con = np.zeros_like(image)
//                con = cv2.drawContours(con, page, -1, (0, 255, 255), 3)
                int max_contours = contours.size() < 5? contours.size() : 5;
                for (int i = 0; i < max_contours; i++) {
                    Imgproc.drawContours(frame, contours, i, new Scalar(255,255,0), 7);
                }

//
//                output = image.copy()
//                Log.d("opencv",String.valueOf(contours.size()));
                if(contours.size() != 0) {
//                    MatOfPoint c = contours.get(0);
                    //     coordinates of the contour
                    MatOfPoint contour_max_area = contours.stream().min(desc_comp).orElseThrow(NoSuchElementException::new);
//                    Log.d("opencv",String.valueOf(Imgproc.contourArea(contour_max_area)));
                    Rect rect = Imgproc.boundingRect(contour_max_area);
                    Imgproc.rectangle(frame,
                            rect.tl(),
                            rect.br(),
                            new Scalar(255,0,0),
                            15);
//                    output = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
                }
                return frame; // inputFrame.rgba();
            }
        });
        if(OpenCVLoader.initDebug()){
            cameraBridgeViewBase.enableView();
        }
    }

    @Override
    protected void onResume() {
        super.onResume();
        cameraBridgeViewBase.enableView();
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        cameraBridgeViewBase.disableView();
    }

    @Override
    protected void onPause() {
        super.onPause();
        cameraBridgeViewBase.enableView();
    }

    @Override
    protected List<? extends CameraBridgeViewBase> getCameraViewList() {
        return Collections.singletonList(cameraBridgeViewBase);
    }

    void getPermission(){
        if(checkSelfPermission(android.Manifest.permission.CAMERA)!= PackageManager.PERMISSION_GRANTED){
            requestPermissions(new String[]{android.Manifest.permission.CAMERA}, 101);
        }
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if(grantResults.length>0 && grantResults[0]!=PackageManager.PERMISSION_GRANTED){
            getPermission();
        }
    }
}