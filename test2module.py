import os
import unittest
import logging
import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *
from slicer.util import VTKObservationMixin
import vtk.util.numpy_support
import SimpleITK as sitk
import sitkUtils
import vtk.util.numpy_support
#
# test2module
#

class test2module(ScriptedLoadableModule):
  """Uses ScriptedLoadableModule base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "test2module"  # TODO: make this more human readable by adding spaces
    self.parent.categories = ["Examples"]  # TODO: set categories (folders where the module shows up in the module selector)
    self.parent.dependencies = []  # TODO: add here list of module names that this module requires
    self.parent.contributors = ["John Doe (AnyWare Corp.)"]  # TODO: replace with "Firstname Lastname (Organization)"
    # TODO: update with short description of the module and a link to online module documentation
    self.parent.helpText = """
This is an example of scripted loadable module. There are 7 functions in this module 
See more information in <a href="https://github.com/organization/projectname#test2module">module documentation</a>.
"""
    # TODO: replace with organization, grant and thanks
    self.parent.acknowledgementText = """
This file was originally developed by Jean-Christophe Fillion-Robin, Kitware Inc., Andras Lasso, PerkLab,
and Steve Pieper, Isomics, Inc. and was partially funded by NIH grant 3P41RR013218-12S1.
"""
 
#
# test2moduleWidget
#

class test2moduleWidget(ScriptedLoadableModuleWidget, VTKObservationMixin):
  """Uses ScriptedLoadableModuleWidget base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent=None):
    if not parent:
      self.parent = slicer.qMRMLWidget()
      self.parent.setLayout(qt.QVBoxLayout())
      self.parent.setMRMLScene(slicer.mrmlScene)
    else:
      self.parent = parent
    self.layout = self.parent.layout()
    if not parent:
      self.setup()
      self.parent.show()
  
  def setup(self):
    #create collapsible button
    collapsibleButton = ctk.ctkCollapsibleButton()
    collapsibleButton.text = "my menu"

    #bind collapsible button to root layout
    self.layout.addWidget(collapsibleButton)

    #new layout for collapsible button
    self.formLayout = qt.QFormLayout(collapsibleButton)
    
    # volume selector
    self.formFrame = qt.QFrame(collapsibleButton)
    
    #select the layout to vertical
    self.formFrame.setLayout(qt.QVBoxLayout())
    
    #bind new frame to existing layout in collapseible menu
    self.formLayout.addWidget(self.formFrame)
   
    #create new volume selector
    self.inputSelector = qt.QLabel("input Volume: ", self.formFrame)

    #bind selector to your frame
    self.formFrame.layout().addWidget(self.inputSelector)

    self.inputSelector = slicer.qMRMLNodeComboBox(self.formFrame)
    self.inputSelector.nodeTypes = (("vtkMRMLScalarVolumeNode"), "") 
    self.inputSelector.addEnabled = False
    self.inputSelector.removeEnabled = False
    self.inputSelector.setMRMLScene(slicer.mrmlScene)

    self.formFrame.layout().addWidget(self.inputSelector)


    # Create buttons
    button01 = qt.QPushButton("Inverse")
    button01.toolTip = "inverse an image"
    button01.connect("clicked(bool)", self.informationButtonClicked01)

    button02 = qt.QPushButton("Laplacian")
    button02.toolTip = "Laplace operator on an image"
    button02.connect("clicked(bool)", self.informationButtonClicked02)

    button03 = qt.QPushButton("Blur")
    button03.toolTip = "Blur the image"
    button03.connect("clicked(bool)", self.informationButtonClicked03)
    
    button04 = qt.QPushButton("Crop 1")
    button04.toolTip = "Crop the image"
    button04.connect("clicked(bool)", self.informationButtonClicked04)

    button05 = qt.QPushButton("Crop 2")
    button05.toolTip = "Crop the image"
    button05.connect("clicked(bool)", self.informationButtonClicked05)

    button06 = qt.QPushButton("ROI Croping")
    button06.toolTip = "Crop the image using ROI"
    button06.connect("clicked(bool)", self.informationButtonClicked06)
     
    button07 = qt.QPushButton("Get size")
    button07.toolTip = "get size of the image"
    button07.connect("clicked(bool)", self.informationButtonClicked07)

    #bind buttons to frame
    self.formFrame.layout().addWidget(button01)
    self.formFrame.layout().addWidget(button02)
    self.formFrame.layout().addWidget(button03)
    self.formFrame.layout().addWidget(button04)
    self.formFrame.layout().addWidget(button05)
    self.formFrame.layout().addWidget(button06)     
    self.formFrame.layout().addWidget(button07)
   
    self.textfield = qt.QTextEdit()
    self.textfield.setReadOnly(True)
    self.formFrame.layout().addWidget(self.textfield)
   
        
  # Function of each button
  # Inverse
  def informationButtonClicked01(self):

    print("myScript Inverse")
    inputVolumeNode  = slicer.util.getNode(self.inputSelector.currentNode().GetName())
    i = inputVolumeNode.GetImageData()
    a = vtk.util.numpy_support.vtk_to_numpy(i.GetPointData().GetScalars())
    a[:] = 100 - a
    i.Modified()

  
  # Laplacian
  def informationButtonClicked02(self):

    # Pull volume from Slicer
    print("myScript Laplacian")
    inputVolumeNode  = slicer.util.getNode(self.inputSelector.currentNode().GetName())
    inputVolumeNodeSceneAddress = inputVolumeNode.GetScene().GetAddressAsString("").replace('Addr=','')
    inputVolumeNodeFullITKAddress = 'slicer:{0}#{1}'.format(inputVolumeNodeSceneAddress,inputVolumeNode.GetID())
    inputImage = sitk.ReadImage(inputVolumeNodeFullITKAddress)
    
    # Process
    filter = sitk.LaplacianRecursiveGaussianImageFilter()
    filter.SetSigma(1)
    outputImage = filter.Execute(inputImage)

    # Push volume to Slicer
    outputVolumeNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLScalarVolumeNode")
    outputVolumeNode.CreateDefaultDisplayNodes()
    outputVolumeNodeSceneAddress = outputVolumeNode.GetScene().GetAddressAsString("").replace('Addr=','')
    outputVolumeNodeFullITKAddress = 'slicer:{0}#{1}'.format(outputVolumeNodeSceneAddress,outputVolumeNode.GetID())
    sitk.WriteImage(outputImage, outputVolumeNodeFullITKAddress)
    slicer.util.setSliceViewerLayers(background = outputVolumeNode)



  # Blur function
  def informationButtonClicked03(self):

    print("myScript Blur")
    parameters = {}
    parameters['outputVolume'] = 'vtkMRMLScalarVolumeNode1'
    parameters['inputVolume'] = 'vtkMRMLScalarVolumeNode1'
    parameters['sigma'] = 3
    slicer.cli.run(slicer.modules.gaussianblurimagefilter, None, parameters)


  # Crop 1
  def informationButtonClicked04(self):

    # Pull volume from Slicer
    print("My script crop 1 ")
    inputVolumeNode  = slicer.util.getNode(self.inputSelector.currentNode().GetName())
    inputVolumeNodeSceneAddress = inputVolumeNode.GetScene().GetAddressAsString("").replace('Addr=','')
    inputVolumeNodeFullITKAddress = 'slicer:{0}#{1}'.format(inputVolumeNodeSceneAddress,inputVolumeNode.GetID())
    inputImage = sitk.ReadImage(inputVolumeNodeFullITKAddress)

    croppedImageFnm = "C:/javaneh/0_Slicer/myCroppedVolume1.nrrd" # give the path for saving result image
    
    # Process
    cropper = sitkUtils.sitk.CropImageFilter()
    croppingBounds = [[20, 20, 20],[40, 40, 40]] # change for different croping result
    
    cropper.SetLowerBoundaryCropSize(croppingBounds[0])
    cropper.SetUpperBoundaryCropSize(croppingBounds[1])
    
    croppedImage = cropper.Execute(inputImage)
    
    # Push volume to Slicer
    outputVolumeNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLScalarVolumeNode")
    outputVolumeNode.CreateDefaultDisplayNodes()
    outputVolumeNodeSceneAddress = outputVolumeNode.GetScene().GetAddressAsString("").replace('Addr=','')
    outputVolumeNodeFullITKAddress = 'slicer:{0}#{1}'.format(outputVolumeNodeSceneAddress,outputVolumeNode.GetID())
    sitk.WriteImage(croppedImage, outputVolumeNodeFullITKAddress)
    slicer.util.setSliceViewerLayers(background = outputVolumeNode)

    
    # save cropped image
    properties = {}
    properties["fileType"] = ".nrrd"
    slicer.util.saveNode(outputVolumeNode, croppedImageFnm, properties)
    print(" All tasks are done!  ")
    
   
  # Crop 2
  def informationButtonClicked05(self):
    
    # Pull volume from Slicer
    print(" My script crop 2")
    inputVolumeNode  = slicer.util.getNode(self.inputSelector.currentNode().GetName())
    inputVolumeNodeSceneAddress = inputVolumeNode.GetScene().GetAddressAsString("").replace('Addr=','')
    inputVolumeNodeFullITKAddress = 'slicer:{0}#{1}'.format(inputVolumeNodeSceneAddress,inputVolumeNode.GetID())
    inputImage = sitk.ReadImage(inputVolumeNodeFullITKAddress)
    
    # Process
    croppedImagePath = "C:/javaneh/0_Slicer/myCroppedVolume2.nrrd" # give the path for saving result image
    center = (128, 128, 65)
    croppedImage = inputImage[center[0]-80:center[0]+50, center[1]-50:center[1]+50, center[2]-55:center[2]+55] # change for different croping result
    
    # Push volume to Slicer
    outputVolumeNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLScalarVolumeNode")
    outputVolumeNode.CreateDefaultDisplayNodes()
    outputVolumeNodeSceneAddress = outputVolumeNode.GetScene().GetAddressAsString("").replace('Addr=','')
    outputVolumeNodeFullITKAddress = 'slicer:{0}#{1}'.format(outputVolumeNodeSceneAddress,outputVolumeNode.GetID())
    sitk.WriteImage(croppedImage, outputVolumeNodeFullITKAddress)
    slicer.util.setSliceViewerLayers(background = outputVolumeNode)

    
    # save cropped image
    properties = {}
    properties["fileType"] = ".nrrd"
    slicer.util.saveNode(outputVolumeNode, croppedImagePath, properties)
    print(" All tasks are done!  ")
   

  #ROI crop
  def informationButtonClicked06(self):

    print("myScript ROI crop")
    volumeNode  = slicer.util.getNode(self.inputSelector.currentNode().GetName())

    logic = slicer.modules.volumerendering.logic()
    displayNode = logic.CreateVolumeRenderingDisplayNode()
    displayNode.UnRegister(slicer.mrmlScene)  # See https://www.slicer.org/wiki/Documentation/Nightly/Developers/Tutorials/MemoryManagement     ref: https://discourse.slicer.org/t/3d-view-interactive-roi-cropping/17735/11
    slicer.mrmlScene.AddNode(displayNode)
    volumeNode.AddAndObserveDisplayNodeID(displayNode.GetID())
    logic.UpdateDisplayNodeFromVolumeNode(displayNode, volumeNode)
    
    displayNode.SetVisibility(True)  # Volume Rendering shown in 3D view
    displayNode.SetCroppingEnabled(True)  # Cropping Enabled
    displayNode.GetROINode().SetDisplayVisibility(True)  # Show ROI used for cropping Volume Rendering


  
  # Show the size of data
  def informationButtonClicked07(self):

    print("myScript size")
    n = slicer.util.getNode(self.inputSelector.currentNode().GetName())
    i = n.GetImageData()
    a = vtk.util.numpy_support.vtk_to_numpy(i.GetPointData().GetScalars())
    p = a.size
    self.textfield.insertPlainText(str(p)+"\n")







   
    
    


















    
    
    