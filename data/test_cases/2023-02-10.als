
abstract sig Obj { get: FName -> {Obj + Val } }
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
sig Professor extends Obj {}
sig Student extends Obj {}
sig User extends Obj {}
sig Message extends Obj {}
sig Group extends Obj {}
sig Chat extends Obj {}
private one sig tags extends FName {}
private one sig text extends FName {}
private one sig Authorship extends FName {}
private one sig type_String extends Val {}
private one sig administrator extends FName {}
private one sig Membership extends FName {}
private one sig Releated extends FName {}
private one sig Posted extends FName {}

fun ProfessorSubsCD: set Obj { Professor }
fun StudentSubsCD: set Obj { Student }
fun UserSubsCD: set Obj { User +  Professor +  Student }
fun MessageSubsCD: set Obj { Message }
fun GroupSubsCD: set Obj { Group }
fun ChatSubsCD: set Obj { Chat }

fact messageConstraint {
  all m : Message, c : Chat  | 
    m in c.get[Posted] implies 
      m.get[Authorship] in 
        { u: User | some g: Group | g in c.get[Releated] and u in g.get[Membership] }
}

fact {

#Group = 2
no Professor.get[FName]
no Student.get[FName]
no User.get[FName]
}

pred cd {
ObjAttrib[Message, tags, UserSubsCD]
ObjAttrib[Message, text, type_String]
ObjAttrib[Group, administrator, StudentSubsCD]


ObjFNames[Message, tags + text + Authorship]
ObjFNames[Group, administrator + Membership]
ObjFNames[Chat, Releated + Posted]


Obj = Professor + Student + User + Message + Group + Chat





ObjLUAttrib[MessageSubsCD, Authorship, UserSubsCD, 1, 1]
ObjLAttrib[GroupSubsCD, Membership, UserSubsCD, 1]
ObjLUAttrib[ChatSubsCD, Releated, GroupSubsCD, 1, 1]
ObjLAttrib[ChatSubsCD, Posted, MessageSubsCD, 1]
ObjL[UserSubsCD, Authorship, MessageSubsCD, 0]
ObjL[UserSubsCD, Membership, GroupSubsCD, 1]
ObjLU[GroupSubsCD, Releated, ChatSubsCD, 1, 1]
ObjL[MessageSubsCD, Posted, ChatSubsCD, 1]
}
run cd for 10
