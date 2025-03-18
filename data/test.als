abstract sig Obj { get: FName -> {Obj + Val + EnumVal} }
abstract sig FName {}
abstract sig Val {}
abstract sig EnumVal {}

pred ObjAttrib[objs: set Obj, fName: one FName,
fType: set {Obj + Val + EnumVal}] {
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


sig Employee extends Obj {}
sig Task extends Obj {}
sig Manager extends Obj {}


private one sig kind extends FName {}
private one sig id extends FName {}
private one sig managedBy extends FName {}
private one sig tasks extends FName {}
private one sig type_Int extends Val {}
private one sig startDate extends FName {}
private one sig type_Date extends Val {}


private one sig enum_PositionKind_MANAGER extends EnumVal {}
private one sig enum_PositionKind_EMPLOYEE extends EnumVal {}


fun EmployeeSubsCD: set Obj { Employee +  Manager }
fun TaskSubsCD: set Obj { Task }
fun ManagerSubsCD: set Obj { Manager }


fun PositionKindEnumCD: set EnumVal {
	enum_PositionKind_MANAGER +
	enum_PositionKind_EMPLOYEE 
}

pred cd {

ObjAttrib[Employee, kind, PositionKindEnumCD]
ObjAttrib[Employee, id, type_Int]
ObjAttrib[Task, startDate, type_Date]
ObjAttrib[Manager, kind, PositionKindEnumCD]
ObjAttrib[Manager, id, type_Int]

ObjFNames[Employee, kind + id + managedBy + tasks]
ObjFNames[Task, startDate]
ObjFNames[Manager, kind + id + managedBy + tasks]


Obj = Employee + Task + Manager


ObjLUAttrib[EmployeeSubsCD, managedBy, ManagerSubsCD, 0, 1]
ObjLAttrib[EmployeeSubsCD, tasks, TaskSubsCD, 0]
ObjL[ManagerSubsCD, managedBy, EmployeeSubsCD, 0]
ObjLU[TaskSubsCD, tasks, EmployeeSubsCD, 1, 1]
}

















