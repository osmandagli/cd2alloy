abstract sig Obj { get: FName -> {Obj + Val} }
abstract sig FName {}
abstract sig Val {}
pred ObjAttrib[objs: set Obj, fName: one FName,
fType: set {Obj + Val }] {
objs.get[fName] in fType
all o: objs| one o.get[fName] }

pred ObjFNames[objs: set Obj, fNames:set FName] {
no objs.get[FName - fNames] }

pred BidiAssoc[left: set Obj, lFName:one FName,
 right: set Obj, rFName:one FName] {
 all l: left | all r: l.get[lFName] | l in r.get[rFName]
 all r: right | all l: r.get[rFName] | r in l.get[lFName] }

 pred Composition[compos: Obj->Obj, right: set Obj] {
 all r: right | lone compos.r }

 fun rel[wholes: set Obj, fn: FName] : Obj->Obj {
    {o1:Obj,o2:Obj|o1->fn->o2 in wholes <: get} }


pred ObjUAttrib[objs: set Obj, fName:one FName, fType:set Obj, up: Int] {
objs.get[fName] in fType
all o: objs| (#o.get[fName] =< up) }

pred ObjLAttrib[objs: set Obj, fName: one FName, fType: set Obj, low: Int] {
objs.get[fName] in fType
all o: objs | (#o.get[fName] >= low) }

pred ObjLUAttrib[objs:set Obj, fName:one FName, fType:set Obj,
 low: Int, up: Int] {
 ObjLAttrib[objs, fName, fType, low]
 ObjUAttrib[objs, fName, fType, up] }

pred ObjL[objs: set Obj, fName:one FName, fType: set Obj, low: Int] {
all r: objs | # { l: fType | r in l.get[fName]} >= low }

pred ObjU[objs: set Obj, fName:one FName, fType: set Obj, up: Int] {
all r: objs | # { l: fType | r in l.get[fName]} =< up }

pred ObjLU[objs: set Obj, fName:one FName, fType: set Obj,
low: Int, up: Int] {
ObjL[objs, fName, fType, low]
 ObjU[objs, fName, fType, up] }