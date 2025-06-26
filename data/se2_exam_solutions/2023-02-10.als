
/*
Obj represents classes
Get return the corresponding value
*/
abstract sig Obj { get: FName -> {Obj + Val} }
// FName represents associations
abstract sig FName {}
// Val represents unknown types
abstract sig Val {}

/*
This predicates ensures that if you have a field for a class’s attribute, ObjAttrib guarantees that every object retrieves exactly one value and that the value is of the correct type.
*/
pred ObjAttrib[objs: set Obj, fName: one FName, fType: set {Obj + Val}] {
objs.get[fName] in fType
all o: objs| one o.get[fName]
}

/*
This predicate ensures that no fields outside the specified set.
*/

pred ObjFNames[objs: set Obj, fNames:set FName] {
no objs.get[FName - fNames]
}

/*
This predicate models a bidirectional association between two sets of objects.
*/

pred BidiAssoc[left: set Obj, lFName:one FName, right: set Obj, rFName:one FName] {
all l: left | all r: l.get[lFName] | l in r.get[rFName]
all r: right | all l: r.get[rFName] | r in l.get[lFName]
}

/*
For every part object (member of right), there is at most one whole object that points to it via the compos relation.
*/

pred Composition[compos: Obj->Obj, right: set Obj] {
all r: right | lone compos.r
}

/*
It returns the set of all ordered pairs (o1, o2) such that:

o1 is in the set wholes,

o1 has a field named fn (via the get relation), and

o2 is the value associated with fn for o1.

This predicate ensures that o2 exists with o1->fn->o2. Used for composition
for ensuring o2 cannot exists without o1.
*/

fun rel[wholes: set Obj, fn: FName] : Obj->Obj {
{o1:Obj,o2:Obj|o1->fn->o2 in wholes <: get}
}

/*
Ending with Attrib makes association its attribute
Without Attrib just makes a constraint for the opposition attribute.
*/

pred ObjUAttrib[objs: set Obj, fName:one FName, fType:set Obj, up: Int] {
objs.get[fName] in fType
all o: objs| (#o.get[fName] =< up)
}

pred ObjLAttrib[objs: set Obj, fName: one FName, fType: set Obj, low: Int] {
objs.get[fName] in fType
all o: objs | (#o.get[fName] >= low)
}

pred ObjLUAttrib[objs:set Obj, fName:one FName, fType:set Obj,low: Int, up: Int] {
ObjLAttrib[objs, fName, fType, low]
ObjUAttrib[objs, fName, fType, up]
}

pred ObjL[objs: set Obj, fName:one FName, fType: set Obj, low: Int] {
all r: objs | # { l: fType | r in l.get[fName]} >= low
}

pred ObjU[objs: set Obj, fName:one FName, fType: set Obj, up: Int] {
all r: objs | # { l: fType | r in l.get[fName]} =< up
}

pred ObjLU[objs: set Obj, fName:one FName, fType: set Obj,low: Int, up: Int] {
ObjL[objs, fName, fType, low]
ObjU[objs, fName, fType, up]
}

// Funtion to get the inverse
fun getInv[target: Obj, field: FName]: set Obj {
{ o: Obj | target in o.get[field] }
}
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
  all m : Message, c : Chat | 
    m in c.get[Posted] implies 
      m.get[Authorship] in 
        getInv[c, Releated].get[Membership]
}

fact {

#User = 2
#Message = 2
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
ObjFNames[Group, administrator + Membership + Releated]
ObjFNames[Chat, Posted]


Obj = Professor + Student + User + Message + Group + Chat





ObjLUAttrib[MessageSubsCD, Authorship, UserSubsCD, 1, 1]
ObjLAttrib[GroupSubsCD, Membership, UserSubsCD, 1]
ObjLUAttrib[GroupSubsCD, Releated, ChatSubsCD, 1, 1]
ObjLAttrib[ChatSubsCD, Posted, MessageSubsCD, 1]
ObjL[UserSubsCD, Authorship, MessageSubsCD, 0]
ObjL[UserSubsCD, Membership, GroupSubsCD, 1]
ObjLU[ChatSubsCD, Releated, GroupSubsCD, 1, 1]
ObjL[MessageSubsCD, Posted, ChatSubsCD, 1]
}
run cd for 10
