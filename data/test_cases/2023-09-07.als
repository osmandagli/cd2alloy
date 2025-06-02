
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
sig VAT extends Obj {}
sig VAT4 extends Obj {}
sig VAT10 extends Obj {}
sig VAT22 extends Obj {}
sig Product extends Obj {}
sig Meat extends Obj {}
sig BasicGrocery extends Obj {}
sig Other extends Obj {}
sig Username extends Obj {}
sig Password extends Obj {}
sig User extends Obj {}
sig ProductSet extends Obj {}
sig Cart extends Obj {}
sig Order extends Obj {}
sig UserAccount extends Obj {}
sig OnlineShop extends Obj {}
private one sig vat extends FName {}
private one sig accounts extends FName {}
private one sig products extends FName {}
private one sig uname extends FName {}
private one sig pwd extends FName {}
private one sig orders extends FName {}
private one sig cart extends FName {}

fun VATSubsCD: set Obj { VAT +  VAT4 +  VAT10 +  VAT22 }
fun VAT4SubsCD: set Obj { VAT4 }
fun VAT10SubsCD: set Obj { VAT10 }
fun VAT22SubsCD: set Obj { VAT22 }
fun ProductSubsCD: set Obj { Product +  Meat +  BasicGrocery +  Other }
fun MeatSubsCD: set Obj { Meat }
fun BasicGrocerySubsCD: set Obj { BasicGrocery }
fun OtherSubsCD: set Obj { Other }
fun UsernameSubsCD: set Obj { Username }
fun PasswordSubsCD: set Obj { Password }
fun UserSubsCD: set Obj { User }
fun ProductSetSubsCD: set Obj { ProductSet +  Cart +  Order }
fun CartSubsCD: set Obj { Cart }
fun OrderSubsCD: set Obj { Order }
fun UserAccountSubsCD: set Obj { UserAccount }
fun OnlineShopSubsCD: set Obj { OnlineShop }


fact InOnlineShop {
	one shop : OnlineShop | 
	all user : UserAccount  | 	user in shop.get[accounts] and 
							user.get[cart].get[products] in shop.get[products]
							and user.get[orders].get[products] in shop.get[products]
}

fact uniqueUserName {
	all os: OnlineShop | no disj ua1, ua2 : os.get[accounts] | ua1.get[uname] = ua2.get[uname]
}

pred updateAccound [ua, ua2 : UserAccount, p: Product] {

	not (p in ua.get[cart].get[products])
	ua2.get[uname] = ua.get[uname]
	ua2.get[pwd] = ua.get[pwd]
	ua2.get[orders] = ua.get[orders]
	some c: Cart | c.get[proucts] = ua.get[cart].get[products] + p and
				ua2.get[cart] = c
	some u: User | u.get[accounts] = (getInv[u, accounts]).get[accounts] - ua + ua2

}

fun timesBought [ua: Username, p: Product] : Int {
	let orders = {u: ua.get[orders]| p in o.get[products] } | #orders
}


fact {

	no VAT.get[FName]
	no VAT4.get[FName]
	no VAT10.get[FName]
	no VAT22.get[FName]
	no Username.get[FName]
	no Password.get[FName]
	no VAT

	no Product

	all o: Order | #o.get[products] > 0
	all c: Cart | #c.get[products] > 0
	#User = 2
}

pred cd {
ObjAttrib[Meat, vat, VAT10SubsCD]
ObjAttrib[BasicGrocery, vat, VAT4SubsCD]
ObjAttrib[Other, vat, VAT22SubsCD]
ObjAttrib[UserAccount, uname, UsernameSubsCD]
ObjAttrib[UserAccount, pwd, PasswordSubsCD]
ObjAttrib[UserAccount, orders, OrderSubsCD]


ObjFNames[Meat, vat + vat]
ObjFNames[BasicGrocery, vat + vat]
ObjFNames[Other, vat + vat]
ObjFNames[User, accounts]
ObjFNames[ProductSet, products]
ObjFNames[Cart, products]
ObjFNames[Order, products]
ObjFNames[UserAccount, uname + pwd + orders + cart]
ObjFNames[OnlineShop, products + accounts]


Obj = VAT4 + VAT10 + VAT22 + Meat + BasicGrocery + Other + Username + Password + User + ProductSet + Cart + Order + UserAccount + OnlineShop





ObjLUAttrib[ProductSubsCD, vat, VATSubsCD, 1, 1]
ObjLAttrib[UserSubsCD, accounts, UserAccountSubsCD, 1]
ObjLAttrib[ProductSetSubsCD, products, ProductSubsCD, 0]
ObjLUAttrib[UserAccountSubsCD, cart, CartSubsCD, 1, 1]
ObjLAttrib[OnlineShopSubsCD, products, ProductSubsCD, 1]
ObjLAttrib[OnlineShopSubsCD, accounts, UserAccountSubsCD, 1]
ObjLU[VATSubsCD, vat, ProductSubsCD, 1, 1]
ObjLU[UserAccountSubsCD, accounts, UserSubsCD, 1, 1]
ObjLU[ProductSubsCD, products, ProductSetSubsCD, 1, 1]
ObjLU[CartSubsCD, cart, UserAccountSubsCD, 1, 1]
ObjLU[ProductSubsCD, products, OnlineShopSubsCD, 1, 1]
ObjLU[UserAccountSubsCD, accounts, OnlineShopSubsCD, 1, 1]
}
run cd for 20
