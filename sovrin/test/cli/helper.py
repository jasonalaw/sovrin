import os
from plenum.test.cli.test_cli_client_port import initDirWithGenesisTxns
from plenum.test.eventually import eventually

from sovrin.common.plugin_helper import writeAnonCredPlugin
from sovrin.common.txn import USER, ROLE
from sovrin.test.helper import TestNode, TestClient

from plenum.test.cli.helper import TestCliCore, newCLI as newPlenumCLI, \
    assertAllNodesCreated, checkAllNodesStarted
from plenum.test.testable import Spyable
from plenum.common.txn import TARGET_NYM, ROLE
from sovrin.cli.cli import SovrinCli


@Spyable(methods=[SovrinCli.print, SovrinCli.printTokens])
class TestCLI(SovrinCli, TestCliCore):
    pass


def newCLI(looper, tdir, subDirectory=None, conf=None, poolDir=None,
           domainDir=None):
    tempDir = os.path.join(tdir, subDirectory) if subDirectory else tdir
    if poolDir or domainDir:
        initDirWithGenesisTxns(tempDir, conf, poolDir, domainDir)
    writeAnonCredPlugin(tempDir, reloadTestModules=True)
    return newPlenumCLI(looper, tempDir, cliClass=TestCLI,
                        nodeClass=TestNode, clientClass=TestClient, config=conf)


def sendNym(cli, nym, role):
    cli.enterCmd("send NYM {}={} "
                 "{}={}".format(TARGET_NYM, nym,
                                ROLE, role))


def checkGetNym(cli, nym):
    printeds = ["Getting nym {}".format(nym), "Transaction id for NYM {} is ".format(nym)]
    checks = [x in cli.lastCmdOutput for x in printeds]
    assert all(checks)
    # TODO: These give NameError, don't know why
    # assert all([x in cli.lastCmdOutput for x in printeds])
    # assert all(x in cli.lastCmdOutput for x in printeds)


def chkNymAddedOutput(cli, nym):
    checks = [x['msg'] == "Nym {} added".format(nym) for x in cli.printeds]
    assert any(checks)


def checkConnectedToEnv(cli):
    # TODO: Improve this
    assert "now connected to" in cli.lastCmdOutput


def ensureConnectedToTestEnv(cli):
    if not cli.activeEnv:
        cli.enterCmd("connect test")
        cli.looper.run(
            eventually(checkConnectedToEnv, cli, retryWait=1, timeout=10))


def ensureNymAdded(cli, nym, role=USER):
    ensureConnectedToTestEnv(cli)
    cli.enterCmd("send NYM {dest}={nym} {ROLE}={role}".format(
        dest=TARGET_NYM, nym=nym, ROLE=ROLE, role=role))
    cli.looper.run(
        eventually(chkNymAddedOutput, cli, nym, retryWait=1, timeout=10))
    cli.enterCmd("send GET_NYM {dest}={nym}".format(dest=TARGET_NYM, nym=nym))
    cli.looper.run(eventually(checkGetNym, cli, nym, retryWait=1, timeout=10))


def ensureNodesCreated(cli, nodeNames):
    cli.enterCmd("new node all")
    # TODO: Why 2 different interfaces one with list and one with varags
    assertAllNodesCreated(cli, nodeNames)
    checkAllNodesStarted(cli, *nodeNames)
