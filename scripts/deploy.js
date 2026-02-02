async function main() {
  console.log("MedStrate Architecture: Local Node Active");
}
main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
