/*	
	Obj represents classes
	Get return the corresponding value 
*/
abstract sig Obj { get: FName -> {Obj} }
// FName represents associations
abstract sig FName {}

/* 
	This predicates ensures that if you have a field for a class’s attribute, ObjAttrib guarantees that every object retrieves exactly one value and that the value is of the correct type.
*/
pred ObjAttrib[objs: set Obj, fName: one FName, fType: set {Obj}] {
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