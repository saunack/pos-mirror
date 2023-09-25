import 'dart:developer';

import 'package:camera/camera.dart';
import 'package:get/state_manager.dart';

class ScanController extends GetxController{
 final RxBool _isInitialized = RxBool(false);
 late CameraController _cameraController;
 late List<CameraDescription> _cameras;

 bool get isInitialized => _isInitialized.value;
 CameraController get cameraController => _cameraController;

 @override
 void onInit(){
   super.onInit();
   _initCamera();
 }

 @override
 void dispose(){
   _isInitialized.value = false;
   _cameraController.dispose();
   super.dispose();
 }

 Future<void> _initCamera() async{
   _cameras = await availableCameras();

   _cameraController = CameraController(_cameras[0], ResolutionPreset.max);
   _cameraController.initialize().then((_) {
     _isInitialized.value = true;
   }).catchError((Object e) {
     if (e is CameraException) {
       switch (e.code) {
         case 'CameraAccessDenied':
         // Handle access errors here.
           break;
         default:
         // Handle other errors here.
           break;
       }
     }
   });
 }


}