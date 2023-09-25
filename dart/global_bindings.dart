

import 'dart:developer';

import 'package:get/instance_manager.dart';
import 'package:pos_mirror/scan_controller.dart';

class GlobalBindings extends Bindings{
  @override
  void dependencies(){
    Get.lazyPut<ScanController>(() => ScanController());
  }
}