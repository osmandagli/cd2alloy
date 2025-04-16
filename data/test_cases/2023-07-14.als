
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
sig Area extends Obj {}
sig CandidateInfo extends Obj {}
sig Election extends Obj {}
sig Race extends Obj {}
sig Candidate extends Obj {}
sig Party extends Obj {}
sig FilledPreference extends Obj {}
sig BlankPreference extends Obj {}
sig Preference extends Obj {}
sig Ballot extends Obj {}
sig VoteTracker extends Obj {}
private one sig hasRaces extends FName {}
private one sig hasCandidate extends FName {}
private one sig info extends FName {}
private one sig affiliated extends FName {}
private one sig votes extends FName {}
private one sig validity extends FName {}
private one sig post extends FName {}
private one sig stores extends FName {}
private one sig inBallot extends FName {}
private one sig e extends FName {}
private one sig name extends FName {}
private one sig type_String extends Val {}
private one sig area extends FName {}
private one sig enum_Validity_valid extends EnumVal {}
private one sig enum_Validity_invalid extends EnumVal {}
fun AreaSubsCD: set Obj { Area }
fun CandidateInfoSubsCD: set Obj { CandidateInfo }
fun ElectionSubsCD: set Obj { Election }
fun RaceSubsCD: set Obj { Race }
fun CandidateSubsCD: set Obj { Candidate }
fun PartySubsCD: set Obj { Party }
fun FilledPreferenceSubsCD: set Obj { FilledPreference }
fun BlankPreferenceSubsCD: set Obj { BlankPreference }
fun PreferenceSubsCD: set Obj { Preference +  FilledPreference +  BlankPreference }
fun BallotSubsCD: set Obj { Ballot }
fun VoteTrackerSubsCD: set Obj { VoteTracker }


fun ValidityEnumCD: set EnumVal {
	enum_Validity_valid+
	enum_Validity_invalid 
}


fun RaceCompFieldsCD:Obj->Obj {
   rel[ElectionSubsCD, hasRaces]
}
fact {

no Validity.get[FName]
no Area.get[FName]
no CandidateInfo.get[FName]
no Candidate.get[FName]
no FilledPreference.get[FName]
no BlankPreference.get[FName]
no Ballot.get[FName]
no VoteTracker.get[FName]
}

pred cd {
ObjAttrib[Candidate, info, CandidateInfoSubsCD]
ObjAttrib[FilledPreference, votes, CandidateSubsCD]
ObjAttrib[FilledPreference, post, RaceSubsCD]
ObjAttrib[FilledPreference, validity, ValidityEnumCD]
ObjAttrib[BlankPreference, post, RaceSubsCD]
ObjAttrib[Preference, post, RaceSubsCD]
ObjAttrib[Ballot, e, ElectionSubsCD]
ObjAttrib[Ballot, name, type_String]
ObjAttrib[VoteTracker, area, AreaSubsCD]


ObjFNames[Election, hasRaces]
ObjFNames[Race, hasCandidate]
ObjFNames[Candidate, info]
ObjFNames[Party, affiliated]
ObjFNames[FilledPreference, votes + validity + post + stores + inBallot]
ObjFNames[BlankPreference, post + stores + inBallot]
ObjFNames[Preference, post + stores + inBallot]
ObjFNames[Ballot, e + name]
ObjFNames[VoteTracker, area]


Obj = Area + CandidateInfo + Election + Race + Candidate + Party + FilledPreference + BlankPreference + Preference + Ballot + VoteTracker


Composition[RaceCompFieldsCD, RaceSubsCD]


ObjLAttrib[ElectionSubsCD, hasRaces, RaceSubsCD, 1]
ObjLAttrib[RaceSubsCD, hasCandidate, CandidateSubsCD, 1]
ObjLAttrib[PartySubsCD, affiliated, CandidateSubsCD, 1]
ObjLAttrib[PreferenceSubsCD, stores, VoteTrackerSubsCD, 1]
ObjLAttrib[PreferenceSubsCD, inBallot, BallotSubsCD, 1]
ObjLU[RaceSubsCD, hasRaces, ElectionSubsCD, 1, 1]
ObjLU[CandidateSubsCD, hasCandidate, RaceSubsCD, 1, 1]
ObjLU[CandidateSubsCD, affiliated, PartySubsCD, 1, 1]
ObjL[VoteTrackerSubsCD, stores, PreferenceSubsCD, 1]
ObjL[BallotSubsCD, inBallot, PreferenceSubsCD, 1]
}
run cd for 10
