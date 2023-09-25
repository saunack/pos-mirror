import 'dart:developer';

import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:pos_mirror/scan_controller.dart';
import 'package:camera/camera.dart';


class CameraViewer extends StatelessWidget{
  const CameraViewer({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context){
    return GetX<ScanController>(builder: (controller) {
      if (!controller.isInitialized) {
        return Container();
      }
      log("Initialized controller");
      log(Get.height.toString());
      log(Get.width.toString());
      return SizedBox(
        height: Get.height,
        width: Get.width,
        child: CameraPreview(controller.cameraController),
      );
    }
    );
  }
}