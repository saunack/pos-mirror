import 'package:pos_mirror/camera/camera_screen.dart';
import 'package:flutter/material.dart';
import 'package:get/route_manager.dart';
import 'package:pos_mirror/global_bindings.dart';

// stream https://www.youtube.com/watch?v=oqfCCWhNe7s&t=69s
// live detec https://www.youtube.com/watch?v=MxlKKd6kzMc
// alt live https://www.youtube.com/watch?v=7Q_rRAORBhY
void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return GetMaterialApp(
      debugShowCheckedModeBanner: false,
      home: const CameraScreen(),
      title: "Screen detection",
      initialBinding: GlobalBindings(),
    );
  }
}
