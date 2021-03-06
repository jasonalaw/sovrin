import pytest
from plenum.test.cli.helper import assertCliTokens
from prompt_toolkit.contrib.regular_languages.compiler import compile
from plenum.cli.helper import getUtilGrams, getNodeGrams, getClientGrams, getAllGrams
from plenum.test.cli.test_command_reg_ex import getMatchedVariables
from sovrin.cli.helper import getNewClientGrams


@pytest.fixture("module")
def grammar():
    grams = getClientGrams() + getNewClientGrams()
    return compile("".join(grams))


def test_send_nym_with_role(grammar):
    getMatchedVariables(grammar, 'send NYM dest=LNAyBZUjvLF7duhrNtOWgdAKs18nHdbJUxJLT39iEGU= role=SPONSOR')


def test_send_nym_without_role(grammar):
    getMatchedVariables(grammar, 'send NYM dest=LNAyBZUjvLF7duhrNtOWgdAKs18nHdbJUxJLT39iEGU=')


def test_send_attrib_reg_ex(grammar):
    getMatchedVariables(grammar, 'send ATTRIB dest=LNAyBZUjvLF7duhrNtOWgdAKs18nHdbJUxJLT39iEGU= raw={"legal org": "BRIGHAM YOUNG UNIVERSITY, PROVO, UT", "email":"mail@byu.edu"}')


def test_init_attr_repo_reg_ex(grammar):
    getMatchedVariables(grammar, "initialize mock attribute repo")


def test_add_attr_reg_ex(grammar):
    getMatchedVariables(grammar, "add attribute first_name=Tyler,last_name=Ruff,birth_date=12/17/1991,undergrad=True,postgrad=True,expiry_date=12/31/2101 for Tyler")


def test_add_attr_prover_reg_ex(grammar):
    getMatchedVariables(grammar, "attribute known to BYU first_name=Tyler, last_name=Ruff, birth_date=12/17/1991, undergrad=True, postgrad=True, expiry_date=12/31/2101")


def test_send_issuer_key_reg_ex(grammar):
    getMatchedVariables(grammar, "send ISSUER_KEY reference=15")


def test_req_cred_reg_ex(grammar):
    getMatchedVariables(grammar,
                   "request credential Degree version 1.0 from o7NzafnAlkhNaEM5njaH+I7Y19BEbEORmFB13p87zhM= for Tyler")
    getMatchedVariables(grammar,
                        "request credential Degree version 1.0 from utNKIOcuy796g3jc+cQclAYn2/NUWRtyy/4q+EvZqQM= for Tyler")


def test_gen_cred_reg_ex(grammar):
    getMatchedVariables(grammar, "generate credential for Tyler for Degree version 1.0 with uvalue")


def test_store_cred_reg_ex(grammar):
    getMatchedVariables(grammar, "store credential A=avalue, e=evalue, vprimeprime=vprimevalue for credential cred-id as tyler-degree")


def test_list_cred_reg_ex(grammar):
    getMatchedVariables(grammar, "list CRED")


def test_gen_verif_nonce_reg_ex(grammar):
    getMatchedVariables(grammar, "generate verification nonce")


def test_prep_proof_reg_ex(grammar):
    getMatchedVariables(grammar,
                        "prepare proof of degree using nonce "
                        "mynonce for undergrad")


def test_verify_proof_reg_ex(grammar):
    getMatchedVariables(grammar,
                        "verify status is undergrad in proof degreeproof")


def testShowFileCommandRegEx(grammar):
    matchedVars = getMatchedVariables(grammar,
                                      "show sample/faber-invitation.sovrin")
    assertCliTokens(matchedVars, {
        "show_file": "show", "file_path": "sample/faber-invitation.sovrin"})

    matchedVars = getMatchedVariables(grammar,
                                      "show sample/faber-invitation.sovrin ")
    assertCliTokens(matchedVars, {
        "show_file": "show", "file_path": "sample/faber-invitation.sovrin"})


def testLoadFileCommandRegEx(grammar):
    matchedVars = getMatchedVariables(grammar,
                                      "load sample/faber-invitation.sovrin")
    assertCliTokens(matchedVars, {
        "load_file": "load", "file_path": "sample/faber-invitation.sovrin"})

    matchedVars = getMatchedVariables(grammar,
                                      "load sample/faber-invitation.sovrin ")
    assertCliTokens(matchedVars, {
        "load_file": "load", "file_path": "sample/faber-invitation.sovrin"})


def testShowLinkRegEx(grammar):
    matchedVars = getMatchedVariables(grammar, "show link faber")
    assertCliTokens(matchedVars, {"show_link": "show link",
                                  "link_name": "faber"})

    matchedVars = getMatchedVariables(grammar, "show link faber college")
    assertCliTokens(matchedVars, {"show_link": "show link",
                                  "link_name": "faber college"})

    matchedVars = getMatchedVariables(grammar, "show link faber college ")
    assertCliTokens(matchedVars, {"show_link": "show link",
                                  "link_name": "faber college "})


def test_connect_reg_ex(grammar):
    getMatchedVariables(grammar, "connect dummy")
    getMatchedVariables(grammar, "connect test")
    getMatchedVariables(grammar, "connect live")


def testSyncLinkRegEx(grammar):
    matchedVars = getMatchedVariables(grammar, "sync faber")
    assertCliTokens(matchedVars, {"sync_link": "sync", "link_name": "faber"})

    matchedVars = getMatchedVariables(grammar, 'sync "faber"')
    assertCliTokens(matchedVars, {"sync_link": "sync", "link_name": '"faber"'})

    matchedVars = getMatchedVariables(grammar, 'sync "faber" ')
    assertCliTokens(matchedVars, {"sync_link": "sync", "link_name": '"faber" '})


def testAcceptInvitationLinkRegEx(grammar):
    matchedVars = getMatchedVariables(grammar, "accept invitation from faber")
    assertCliTokens(matchedVars, {"accept_link_invite": "accept invitation from",
                                  "link_name": "faber"})

    matchedVars = getMatchedVariables(grammar, 'accept invitation from "faber"')
    assertCliTokens(matchedVars, {"accept_link_invite": "accept invitation from",
                                  "link_name": '"faber"'})

    matchedVars = getMatchedVariables(grammar, 'accept invitation from "faber" ')
    assertCliTokens(matchedVars, {"accept_link_invite": "accept invitation from",
                                  "link_name": '"faber" '})


def testShowClaimRegEx(grammar):
    matchedVars = getMatchedVariables(grammar, "show claim Transcript")
    assertCliTokens(matchedVars, {"show_claim": "show claim",
                                  "claim_name": "Transcript"})

    matchedVars = getMatchedVariables(grammar, 'show claim "Transcript"')
    assertCliTokens(matchedVars, {"show_claim": "show claim",
                                  "claim_name": '"Transcript"'})


def testRequestClaimRegEx(grammar):
    matchedVars = getMatchedVariables(grammar, "request claim Transcript")
    assertCliTokens(matchedVars, {"req_claim": "request claim",
                                  "claim_name": "Transcript"})

    matchedVars = getMatchedVariables(grammar, 'request claim "Transcript"')
    assertCliTokens(matchedVars, {"req_claim": "request claim",
                                  "claim_name": '"Transcript"'})


def testClaimReqRegEx(grammar):
    matchedVars = getMatchedVariables(grammar,
                                      "show claim request Job Application")
    assertCliTokens(matchedVars, {"show_claim_req": "show claim request",
                                  "claim_req_name": "Job Application"})

    matchedVars = getMatchedVariables(grammar,
                                      "show claim request Job Application ")
    assertCliTokens(matchedVars, {"show_claim_req": "show claim request",
                                  "claim_req_name": "Job Application "})

def testSetAttribute(grammar):
    matchedVars = getMatchedVariables(
        grammar, "set first_name to Alice")
    assertCliTokens(matchedVars, {
        "set_attr": "set", "attr_name": "first_name", "attr_value": "Alice"})
