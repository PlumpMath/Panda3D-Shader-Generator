from panda3d.core import loadPrcFileData
loadPrcFileData("","show-frame-rate-meter #t")
loadPrcFileData("","sync-video #f")

from panda3d.core import *
from direct.task import Task
from direct.actor import Actor
from direct.interval.IntervalGlobal import *
import math
import direct.directbase.DirectStart
print PandaSystem.getVersionString()

from shaderBuilder import *



lib=Library(["library"])


#gg=lib.parseGraph("graph/lit.txt")
#lib.saveGraph(gg,"ShadersOut/debug.txt")

#g=lib.loadGraph("ShadersOut/debug.txt")
#s = g.getShader(None,"ShadersOut/debug.sha")

import editor
ed=editor.Editor(lib,"graph/lit.txt")
ed.save("ShadersOut/debug.txt")
builder=ed.previewBuilder()
s = builder.getShader(None,"ShadersOut/debug.sha")


"""
Shader Generator Demo

"""





# Setup an interesting scene graph to run effects on:
base.disableMouse()

#Load the first environment model
environ = loader.loadModel("models/environment")
environ.reparentTo(render)
environ.setScale(0.25,0.25,0.25)
environ.setPos(-8,42,0)

#Task to move the camera
def SpinCameraTask(task):
    angledegrees = task.time * 6.0
    angleradians = angledegrees * (math.pi / 180.0)
    base.camera.setPos(20*math.sin(angleradians),-20.0*math.cos(angleradians),3)
    base.camera.setHpr(angledegrees, 0, 0)
    return Task.cont

taskMgr.add(SpinCameraTask, "SpinCameraTask")

#Load the panda actor, and loop its animation
pandaActor = Actor.Actor("models/panda-model",{"walk":"models/panda-walk4"})
pandaActor.setScale(0.005,0.005,0.005)
pandaActor.reparentTo(render)
pandaActor.loop("walk")

#Create the four lerp intervals needed to walk back and forth
pandaPosInterval1= pandaActor.posInterval(13,Point3(0,-10,0), startPos=Point3(0,10,0))
pandaPosInterval2= pandaActor.posInterval(13,Point3(0,10,0), startPos=Point3(0,-10,0))
pandaHprInterval1= pandaActor.hprInterval(3,Point3(180,0,0), startHpr=Point3(0,0,0))
pandaHprInterval2= pandaActor.hprInterval(3,Point3(0,0,0), startHpr=Point3(180,0,0))

#Create and play the sequence that coordinates the intervals
pandaPace = Sequence(pandaPosInterval1, pandaHprInterval1,
  pandaPosInterval2, pandaHprInterval2, name = "pandaPace")
pandaPace.loop()



#Set up some lights

# A crazy bright spinning red light seems pretty cool
dlight = DirectionalLight('dlight')
dlight.setColor(Vec4(4.9, 0.9, 0.8, 1))
dlight.setSpecularColor(Vec4(0.9, 0.9, 0.8, 10))
dlnp = render.attachNewNode(dlight)
dlnp.setHpr(0, 0, 0)
render.setLight(dlnp)
render.setShaderInput('dlight',dlnp)

dayCycle=dlnp.hprInterval(10.0,Point3(0,360,0))
dayCycle.loop()

# and an ambient light
alight = AmbientLight('alight')
alight.setColor(Vec4(0.2, 0.2, 0.2, 1))
alnp = render.attachNewNode(alight)
render.setLight(alnp)
render.setShaderInput('alight',alnp)







# Setup some interesting shader inputs
# tinting is pretty lame, but its a demo.
# Relly should just use NodePath.setColorScale, and make an effect use that
# but we can demo custom shader inputs and filters this way
environ.setShaderInput('tintColor',Vec4(.2,.3,.5,1))

# this one is auctually useful. It lets you scale the whole scene brightness
# it could be adjusted dynamically, and could be used as part of an HDR scheme
render.setShaderInput('exposure',2)

# this forces hard edged transparency, and thus frees the alpha channel for other stuff
render.setShaderInput('transparancyThreshold',.5)


# disable trasnparency so alpha to bloom filter is not crazy
render.setTransparency(TransparencyAttrib.MNone,100)

pandaActor.setShader(s)


run()
