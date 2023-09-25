import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:pos_mirror/camera/camera_viewer.dart';
import 'package:camera/camera.dart';

class CameraScreen extends StatelessWidget{
  const CameraScreen({Key? key}) : super(key:key);

  @override
  Widget build(BuildContext context){
    return const Stack(
      alignment: Alignment.center,
      children: [
        CameraViewer()
      ],
    );
  }
}