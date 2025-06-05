
/*
Obj represents classes
Get return the corresponding value
*/
abstract sig Obj { get: FName -> {Obj + Val + EnumVal} }
// FName represents associations
abstract sig FName {}
// Val represents unknown types
abstract sig Val {}
// EnumVal represents enum values
abstract sig EnumVal {}

/*
This predicates ensures that if you have a field for a class’s attribute, ObjAttrib guarantees that every object retrieves exactly one value and that the value is of the correct type.
*/
pred ObjAttrib[objs: set Obj, fName: one FName, fType: set {Obj + Val + EnumVal}] {
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
sig Vehicle extends Obj {}
sig Employee extends Obj {}
sig Driver extends Obj {}
sig Insurance extends Obj {}
sig License extends Obj {}
sig Company extends Obj {}
sig Car extends Obj {}
sig Truck extends Obj {}
private one sig regDate extends FName {}
private one sig licensePlate extends FName {}
private one sig drivenBy extends FName {}
private one sig type_Date extends Val {}
private one sig type_String extends Val {}
private one sig ins extends FName {}
private one sig exp extends FName {}
private one sig license extends FName {}
private one sig drives extends FName {}
private one sig kind extends FName {}
private one sig cars extends FName {}
private one sig emps extends FName {}
private one sig enum_InsuranceKind_transport extends EnumVal {}
private one sig enum_InsuranceKind_international extends EnumVal {}
private one sig enum_DrivingExp_beginner extends EnumVal {}
private one sig enum_DrivingExp_expert extends EnumVal {}
fun VehicleSubsCD: set Obj { Vehicle +  Car +  Truck }
fun EmployeeSubsCD: set Obj { Employee +  Driver }
fun DriverSubsCD: set Obj { Driver }
fun InsuranceSubsCD: set Obj { Insurance }
fun LicenseSubsCD: set Obj { License }
fun CompanySubsCD: set Obj { Company }
fun CarSubsCD: set Obj { Car }
fun TruckSubsCD: set Obj { Truck }


fun InsuranceKindEnumCD: set EnumVal {
	enum_InsuranceKind_transport+
	enum_InsuranceKind_international 
}
fun DrivingExpEnumCD: set EnumVal {
	enum_DrivingExp_beginner+
	enum_DrivingExp_expert 
}



fact {

	no License.get[FName]
	no Vehicle
	#Truck.get[drivenBy] = 1
}

pred cd {
ObjAttrib[Driver, exp, DrivingExpEnumCD]
ObjAttrib[Insurance, kind, InsuranceKindEnumCD]
ObjAttrib[Car, licensePlate, type_String]
ObjAttrib[Car, regDate, type_Date]
ObjAttrib[Truck, licensePlate, type_String]
ObjAttrib[Truck, regDate, type_Date]


ObjFNames[Employee, ins]
ObjFNames[Driver, exp + license + drives + ins]
ObjFNames[Insurance, kind]
ObjFNames[Company, cars + emps]
ObjFNames[Car, regDate + licensePlate + drivenBy]
ObjFNames[Truck, regDate + licensePlate + drivenBy]


Obj = Vehicle + Employee + Driver + Insurance + License + Company + Car + Truck





ObjLAttrib[VehicleSubsCD, drivenBy, DriverSubsCD, 0]
ObjLUAttrib[EmployeeSubsCD, ins, InsuranceSubsCD, 1, 1]
ObjLUAttrib[DriverSubsCD, license, LicenseSubsCD, 0, 3]
ObjLUAttrib[DriverSubsCD, drives, VehicleSubsCD, 0, 1]
ObjLAttrib[CompanySubsCD, cars, CarSubsCD, 0]
ObjLAttrib[CompanySubsCD, emps, EmployeeSubsCD, 0]
ObjLU[DriverSubsCD, drivenBy, VehicleSubsCD, 1, 1]
ObjLU[InsuranceSubsCD, ins, EmployeeSubsCD, 1, 1]
ObjLU[LicenseSubsCD, license, DriverSubsCD, 1, 1]
ObjLU[VehicleSubsCD, drives, DriverSubsCD, 1, 1]
ObjLU[CarSubsCD, cars, CompanySubsCD, 0, 1]
ObjL[EmployeeSubsCD, emps, CompanySubsCD, 0]
}
run cd for 10
