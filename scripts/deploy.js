const hre = require("hardhat");

async function main() {
  const MedStrate = await hre.ethers.getContractFactory("MedStrateAudit");
  const contract = await MedStrate.deploy();
  await contract.waitForDeployment();
  console.log("✅ 9-Sigma Contract Deployed to:", await contract.getAddress());
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
