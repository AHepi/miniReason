# Manifest re-verification, computed

Walked the sandbox copy of the published experiment trees (`experiments/diagnostics/{C001-contrast-triple, F002-fork5-raised-clock, B001-bare-and-native}`, `experiments/analyses/{F002-fork5-raised-clock-2026-09-14, B001-arm-inventory-2026-09-14}`) plus every pinned-bytes file copied at its repository path (`docs/`, `src/`, `tools/`). Every recorded digest was re-hashed with sha256; paths were resolved relative to the manifest's own directory first, then to the sandbox root. Verdicts: MATCH, MISMATCH, MISSING, UNPARSED.

## Name-based candidates

- `src/creib/forge/mini/manifest.py`

## `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json`

- format detected: JSON mapping (top-level key 'files_read' -> 64-hex)
- counts: {"MISSING": 122}
- Bases: manifest_dir then sandbox root.

| path | recorded sha256 | verdict | resolution |
|---|---|---|---|
| `F001-fork5-multifamily/occurrence-01/arms.json` | `5165c89e2179b4fa82c8b7f2529063c0ded25c9b4c0466107be17c98e0fc5aa1` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-01/artifacts/daily/bare/cycle01/answer.json` | `44e1de8ffb17a5a986483e84209f3b988c69a0c83f1df63f25f20e9ac0018dbb` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-01/artifacts/daily/mini_fcl/cycle01/account.json` | `61016c4955d08a97f30d21c69d8cd8d7c0af0ba16b5fe61a7aa162bba0bcd6f0` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-01/artifacts/daily/mini_fcl/cycle01/carry.json` | `ece57747fc6f573aedc0695d22c0492864c820b753f3fe82ee47c1597292e587` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-01/artifacts/daily/mini_fcl/cycle01/objection.json` | `837afc39f263be01471367b9c4bae44ce248960e4ebfe48b7e9436cd0d7c5bdf` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-01/artifacts/daily/mini_fcl/cycle01/response.json` | `2fb7525c7ed516096e6c19db528c12372d7edbaf9c9a68dfa7c1bb9f0eeaa3f5` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-01/artifacts/daily/mini_fcl/cycle01/rival.json` | `d2731fe88de3f53a3656f983c75814f8168281edc218cf7fec7c3db7758ebd69` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-01/artifacts/daily/mini_prose/cycle01/account.json` | `6c31a55824b06279f5e11564b47d3688f44b4d32a449708a79a33e979f89c8df` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-01/artifacts/daily/mini_prose/cycle01/carry.json` | `29d1d9caa299708e852e694aaec603e12b80592d1e5af84222685d48bd3b8b3f` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-01/artifacts/daily/mini_prose/cycle01/objection.json` | `16b96dba473d9469946e99533396add0b80118f8cf4eb543862f8140c9da1288` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-01/artifacts/daily/mini_prose/cycle01/response.json` | `9cafb0718055c4c02209978851b3e3dc73274e96f2be2781cb63a92febb970ba` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-01/artifacts/daily/mini_prose/cycle01/rival.json` | `115093ff57135d44019e0bb7a6ee764562c0f7a7ea0677e06f8691e16fd37297` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-01/artifacts/daily/native/cycle01/answer.json` | `c584244b1b1b3e5118367f6892a7a65a1dafdeda4cd80db93fe2eca8bf5bd4d3` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-01/plan.json` | `6992988f7c70c6af9e1df91c5bd30c676ed2bbd1f4cf23ff707489e82b6f7d55` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-02/arms.json` | `32019959b2506763d8061ee033d274857c7593018214f26bb1cb804795588750` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-02/artifacts/daily/bare/cycle01/answer.json` | `f9fccbf0829879365eb9e2590482cd77b1dc21dbb9a89be7446d5e4ce1496843` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-02/artifacts/daily/mini_fcl/cycle01/account.json` | `d42bb4fe95dd750a782409ea27b0967442f841a050b54e9f103a6e314d255931` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-02/artifacts/daily/mini_fcl/cycle01/carry.json` | `b65a344869c39a49b162ebdb68790d44faa606865cef4b62111ee2ac22a31ba0` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-02/artifacts/daily/mini_fcl/cycle01/objection.json` | `de866de7fdbadea24291ecfa6a74027fa6d6b95620005e38752612c3a20cbb09` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-02/artifacts/daily/mini_fcl/cycle01/response.json` | `213d67082128cd0e13fda2b39c45b6f2aa67e863f57a9f0e2b388ecffdeb2d4b` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-02/artifacts/daily/mini_fcl/cycle01/rival.json` | `0ada966d21486a6952db0eeeff99d233246021acc53248eaa7c5f5e651e5d515` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-02/artifacts/daily/mini_prose/cycle01/account.json` | `f464fa0feb6c4cf9d08b43ec65cd7874bf1f07d856690a1bda83b3fb9c265f57` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-02/artifacts/daily/mini_prose/cycle01/carry.json` | `7f9fabdf5fa0a7b12f3545eff8744d3031c2febc55a9289ec0a0a415aadb31cf` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-02/artifacts/daily/mini_prose/cycle01/objection.json` | `02c4d8e4fea7d1c605754c7755eadf6507040dc5961b17c89fca8d9de722556f` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-02/artifacts/daily/mini_prose/cycle01/response.json` | `ba8a3d41440cce94aee5d864bb7e68380f49ab8f91abd4b6f05b0e280b83cf66` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-02/artifacts/daily/mini_prose/cycle01/rival.json` | `84c2c602b38c22ce1f3d3457bd1dac50617f976a088c8d5f5eea065d05cda66f` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-02/plan.json` | `6609038beaa616d7c27467470dde0cb842071c9ec7006530c3f49ffab13ee58e` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-03/arms.json` | `22cd4ea2542f621b68751345cf135e38210b5d654d937efad281c2887dc6dd51` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-03/artifacts/daily/bare/cycle01/answer.json` | `1a0cfda179d837a427ad9e8091c7e658fad96abe9ae98f95d0a8f81c74915d8b` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-03/artifacts/daily/mini_fcl/cycle01/account.json` | `68a181ab635859cb21020a95e9700bd056509d44160b42fa4b8c8cfbe417d55a` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-03/artifacts/daily/mini_fcl/cycle01/carry.json` | `60f477a1782e760594c15b58ee4386121adb0bd3564d4e5e4d578ca890cdb486` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-03/artifacts/daily/mini_fcl/cycle01/objection.json` | `905de875e846cd93b026129e0fa7e41c18a4db0a5e9ccb55192a7518b8746edc` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-03/artifacts/daily/mini_fcl/cycle01/response.json` | `70e09e1f5bdc914237e2a46b33aed70c19277c0ee243f7a2a4e6fce16008c4f4` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-03/artifacts/daily/mini_fcl/cycle01/rival.json` | `4eaf7b12319d74d5a28c22e73a7f13c0248709f9da767fb8832486b0396e4f47` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-03/artifacts/daily/mini_prose/cycle01/account.json` | `9dd02cbe27cab440bd2028bec2ad7a5bb2cdae2ce8589b93d185a670148cc308` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-03/artifacts/daily/mini_prose/cycle01/carry.json` | `cece31dd208559941fd2a735da8e80b11bcb3e66947430bd3a5dac0d524a2e76` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-03/artifacts/daily/mini_prose/cycle01/objection.json` | `5f8b6117dde25213c9e334d9d8f62d1d7cbc93bea1ddf9017f4813e5538c1ad7` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-03/artifacts/daily/mini_prose/cycle01/response.json` | `f89710455a6ee4f231c0db223a63678c2bf18f28d4b80a4916aee596413003dd` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-03/artifacts/daily/mini_prose/cycle01/rival.json` | `ad617038191076557d0caa100fe1c2c808252c72aab8751c11bcde744a2edded` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-03/plan.json` | `5d3d2cd0a6d342f9ef8ea11a4c7e3b26b6ec311af4c835c9cb682a847be86e2d` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-04/arms.json` | `ca5bdcc8a58b6484ca9d5766690a157443884ac374fbc1a921af3b3ed4d5c984` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-04/artifacts/daily/bare/cycle01/answer.json` | `caf27324cf87d3e3f7a5999d35c6035545c5cb0c88297c062dbb474fd9ebb242` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-04/artifacts/daily/mini_fcl/cycle01/account.json` | `f34da0cb4b9a31c5b4072596258b04eb94849fd08380b1899a5cad1e14bc09a6` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-04/artifacts/daily/mini_prose/cycle01/account.json` | `561294d73c77e7778ab70f3fe86033bbda54b3c34b58d31eb401f1928031725a` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-04/artifacts/daily/mini_prose/cycle01/objection.json` | `2896cf1b3bda4e1423c637c05c4197003982e162c63ca06d005cbd81f3675354` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-04/artifacts/daily/mini_prose/cycle01/rival.json` | `09e9828de01550b78b05073041beb53ba1088c6f9708848882740576a60002f5` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-04/plan.json` | `7d06bdaae719af403cf1df715cee213e87ca310ebaf71a85a92ab5f9ba9ffc1f` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-05/arms.json` | `f06eebde55d74c33b4ad2707b0582453db73d9320b21e34e9e9375427f0cb35c` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-05/artifacts/daily/bare/cycle01/answer.json` | `5f8649f563fa59dba1f9e507130ee0470ba3afe7e22127921fe641ccba0d95df` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-05/artifacts/daily/mini_fcl/cycle01/account.json` | `199fdfce722f92d5341a2b28b03c95856bced948fe10704985fd6caeff313ebf` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-05/artifacts/daily/mini_fcl/cycle01/objection.json` | `68257ce650e37d87cc23869e7793e10282aba93bc37c59e8d9d4922b2747ba9e` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-05/artifacts/daily/mini_fcl/cycle01/rival.json` | `7fa39b7cb4264888b550828e662b0127e6b97f0fc62bd704c06cc7fc40795741` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-05/artifacts/daily/mini_prose/cycle01/account.json` | `399e611599467995f5a3fa41c772b23ddc49be66f362aaf9181cdf4285ed4ce3` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-05/artifacts/daily/mini_prose/cycle01/objection.json` | `3796177d5680ea1913ee8eb939fcbc7a755e97204a99926735161dc5e879a53c` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-05/artifacts/daily/mini_prose/cycle01/response.json` | `3066b5652c09dab4fde54829d2dcf7c36f181058f8b62fd3402ab2d7ba3e194b` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-05/artifacts/daily/mini_prose/cycle01/rival.json` | `8872042f76fa0e877e0369decd8b48ec89f38b54a3a05e54907e895352463950` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-05/plan.json` | `4a756b51d9ceb45b787b9741b025104caa5e8e2627bea0d94c85e48622956342` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-06/arms.json` | `80f846ad4e67c2d7ef6eae6ee6a008ef39ef1d806fac581c1e5e0838f43d0b4c` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-06/artifacts/daily/bare/cycle01/answer.json` | `705882f310a357815e8aa76b776b8bd0049cc5776a133f81451189d58b1119c3` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-06/artifacts/daily/mini_fcl/cycle01/account.json` | `a4d341fde4cc7ba67574b09e0720ba91aea9ec131f1189ae7a9f792651be9067` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-06/artifacts/daily/mini_fcl/cycle01/carry.json` | `fbb91d32d6173ccacdfc1f6bcb46cfde3e4eacfa895e4be54a4ebb3302015c7d` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-06/artifacts/daily/mini_fcl/cycle01/objection.json` | `1be20731a470709231d4fdff9cf062c3a1130c6fb0c2bea350346fc541e2753f` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-06/artifacts/daily/mini_fcl/cycle01/response.json` | `25f2997e8bd6433a485fffa01f76e8dcda794c29959e4f802429cf991b158e58` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-06/artifacts/daily/mini_fcl/cycle01/rival.json` | `043882fc7b920ac73f460f4309c7e19dcc8083551d961521c7955a7f1174062f` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-06/artifacts/daily/mini_prose/cycle01/account.json` | `3d7fc6ef6c8d4700a3ddb544651591f9b3624e33ddd405377c9a77d269fa97cd` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-06/artifacts/daily/mini_prose/cycle01/carry.json` | `e38ff0b8ca674e274e84b1df7e3117192777abeb815fadb840b71f88a102a586` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-06/artifacts/daily/mini_prose/cycle01/objection.json` | `314e3fb2551beb9682d90a2f9da1aee903613b8d6de18c91f1e994e912c7d23e` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-06/artifacts/daily/mini_prose/cycle01/response.json` | `c3e46a926e4a1f7e32ad4cd8b904b7278c5e5c42dfb44c9e97eb9692c00064f4` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-06/artifacts/daily/mini_prose/cycle01/rival.json` | `8ce7b1c63f0c77c9a5283a1c219610fdcd1ef487fcdec81b793269b01406a4ea` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-06/plan.json` | `ee565d3fb40bf4c96c555dbb7994c09ce6e1899011d9b53c8b7bd8632f11e8ad` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-07/arms.json` | `16742fd92972a2d3c80b0d061d0eba51c74a644c761ead984d884eaa46a69199` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-07/artifacts/daily/bare/cycle01/answer.json` | `5d22c22df477cba40210537253c905b6d962b9d0a7c8c93589f3d8add529c64e` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-07/artifacts/daily/mini_fcl/cycle01/account.json` | `47f1448f11a7fe22af3d5ce14e965390b2ca6e0aff867962319f68acec12ee71` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-07/artifacts/daily/mini_fcl/cycle01/rival.json` | `2e6699a1fb6a43d2e024223f2a1b6fc0ac52292e221b9344648f12f42bccf64b` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-07/artifacts/daily/mini_prose/cycle01/account.json` | `d21296d960f2d1b8dd853299caba7bdcb816cc8612e02c11eca4ca35c16e9213` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-07/artifacts/daily/mini_prose/cycle01/carry.json` | `92bb3d68e3e8222a659321171608d2e480cd236cd078ace32da9ebeb9ca5e19a` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-07/artifacts/daily/mini_prose/cycle01/objection.json` | `cc83ca89e521eae8552f71f2519d9cd965f31ad3c6284b84790c374e3d3d6de5` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-07/artifacts/daily/mini_prose/cycle01/response.json` | `4bbdddeb83fab3257237d44bb2877df3efb21dec6efbc24b0e2fd825759e3611` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-07/artifacts/daily/mini_prose/cycle01/rival.json` | `ee88630a8354f99c95c5270bd499182db0bc72d34453f0ae565f5ca136ac4c41` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-07/plan.json` | `1e34079c4af43132440d131e5d7a480dabc4cc15fb501cd4c38eeb6d7f97fb3e` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-08/arms.json` | `5f7cab0797a758e7e2de86e113d404f33b7a0e514482a7e8334398f3fec1e3b6` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-08/artifacts/daily/bare/cycle01/answer.json` | `2b9d51b870073f2fd1395027af01eb466207db016ac475e55ccdbcb73df50a32` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-08/artifacts/daily/mini_fcl/cycle01/account.json` | `1c9c81fec4eaecb74a13684d92293a1a8b7fb1c545195e525982045d920d2a75` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-08/artifacts/daily/mini_fcl/cycle01/objection.json` | `b74c3351c02ee4f98590cce6cd984be6d87d88e370dde7d778921a6fe2b87907` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-08/artifacts/daily/mini_fcl/cycle01/response.json` | `2324e79a0a3739e2d57691df66124b9f64444b0c27192b4f15a6c4d7647e3770` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-08/artifacts/daily/mini_fcl/cycle01/rival.json` | `313c6e0876cb4be25b9b0c8b76fcabfc825d0c3ee56b9264d4bda6acac6f58ad` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-08/artifacts/daily/mini_prose/cycle01/account.json` | `e91563ae39a2679e03342edbb5d6d13cc8da753cbcc3a17e3a93cfdd8ef0b46d` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-08/artifacts/daily/mini_prose/cycle01/carry.json` | `a92dec0e7cf88e32694d11395eb2669550f999875cae0d3d0bfccc6ecc7820d8` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-08/artifacts/daily/mini_prose/cycle01/objection.json` | `f4918bfbc72a19806a8fee7b4b8389a6d8e27b8db0c1f438848b2efa702ee306` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-08/artifacts/daily/mini_prose/cycle01/response.json` | `8d72427bb0cc42f61db62dfd6e263c6ab73db6c95525a589b052cf6095a72c49` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-08/artifacts/daily/mini_prose/cycle01/rival.json` | `b7fd76b43708ffbf5419a1db7d65c4e302d5ff37505157655cff10134252bcd7` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-08/plan.json` | `028c551106cc37c6f568fe559c79e784abe7c849f5372447291e22216e61a5f2` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F002-fork5-raised-clock/occurrence-01/arms.json` | `2a181f80eae29f0716be1fdcae1f67c38df38f096b6cbd7c7a344acbdf013b3b` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F002-fork5-raised-clock/occurrence-01/artifacts/daily/mini_fcl/cycle01/account.json` | `1ea4937b3d84e5aa06286e388d54b19d0e9db4e517993ff71b94b2c98c42ee5e` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F002-fork5-raised-clock/occurrence-01/artifacts/daily/mini_fcl/cycle01/objection.json` | `f1a838bfb9f6d172d5c4e3d37645f6c31b757525df47ad198ef0ddc74e449adb` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F002-fork5-raised-clock/occurrence-01/artifacts/daily/mini_fcl/cycle01/rival.json` | `65d7e4485db366af63e30d37aca2b2b8ef8a83e9b6970625bf9ba141de4ee8d2` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F002-fork5-raised-clock/occurrence-01/plan.json` | `bed7e150c5b116fcb60feaf1e9893f39d23c957af815e86c7c3400984f74e995` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F002-fork5-raised-clock/occurrence-02/arms.json` | `117d9584d9c559a5be9e7103ffdcd4864740f89a65aca9ee804b5384fb989cef` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F002-fork5-raised-clock/occurrence-02/artifacts/daily/mini_fcl/cycle01/account.json` | `968aa1c41706a929e97b35590df51f4f6f9b8228b33e3accf9ee4b6e582a2e51` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F002-fork5-raised-clock/occurrence-02/artifacts/daily/mini_fcl/cycle01/carry.json` | `aff3f6ca406a47739ae38526ef96ad601840e2ff6a3af7d5c5a7ae3b7e5b28c1` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F002-fork5-raised-clock/occurrence-02/artifacts/daily/mini_fcl/cycle01/objection.json` | `5d5b6e79dee79b52281c4d166d415e64e4dfef0c28f2956ef60b42518f7d59e2` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F002-fork5-raised-clock/occurrence-02/artifacts/daily/mini_fcl/cycle01/response.json` | `ad579ff00b132485b97455fa171c86b35f1158712bae6ef9fa41bb4b594d42e0` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F002-fork5-raised-clock/occurrence-02/artifacts/daily/mini_fcl/cycle01/rival.json` | `f18b99266bacec85a48c89bee4496f971be0265a7115361cb9ffc69917ab1a8b` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F002-fork5-raised-clock/occurrence-02/plan.json` | `a4420dfbaff1ea9f5a3971be1f2b2ac9396e7edca7fde70daec9a49a39c7ef54` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `H005-open-prose-commitments/occurrence-01/artifacts/daily/bare/cycle01/answer.json` | `e28f6bd07d8acab50b870d613dcca840c8a1ef96f4c8ac99dac61baa4ded13c7` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `H005-open-prose-commitments/occurrence-01/artifacts/daily/matched/cycle01/account.json` | `4a53987178e4fcaf1ea3f3f61602c5cc50845d1bbaa657cf58827e65decad544` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `H005-open-prose-commitments/occurrence-01/artifacts/daily/matched/cycle01/carry.json` | `19078bf2ed169e74e18e9a682795f3fb5f8c63bf3bb1d53297a26fefa3970526` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `H005-open-prose-commitments/occurrence-01/artifacts/daily/matched/cycle01/objection.json` | `0bbcb5ee57a41ef655f687d3b0f8d9f8ffa399c893d48dae0995c72eb0e5bf8f` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `H005-open-prose-commitments/occurrence-01/artifacts/daily/matched/cycle01/response.json` | `dcd92f6694e2e0f216e24acd013515dcb4d30418a7cc371ae70a7a5e11b29684` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `H005-open-prose-commitments/occurrence-01/artifacts/daily/matched/cycle01/rival.json` | `aebb15d63ba6eebdc354896f6f113643df3e64e2081b2c702d09023a61afa167` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_fcl/cycle01/account.json` | `b8de6a8d579c358cade3296a7e8260a03c6e80269cd0486aae43c134999732e6` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_fcl/cycle01/carry.json` | `cfd3844e4207455171e31093b1f0c57ca0ca11ce1e456d0639b34d62a3401e79` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_fcl/cycle01/objection.json` | `810913b5c31f94a4d697da0e90e74205ac6b7abc7b217d44188852f2562110db` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_fcl/cycle01/response.json` | `a1d4f48d5246608ade51b63604beafc82de9770465d2a7fd7c2340ee8a4e55d3` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_fcl/cycle01/rival.json` | `b0b15d8d44c7dcd706879a9ced41e3f26a592ec5a25c2a961e01e32ea748e8cd` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_prose/cycle01/account.json` | `11bdb5753d4fe7e0bcf2b357cf37afe751e38157e9f1d676f9e32ce63e3f1005` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_prose/cycle01/carry.json` | `4a48f31e01d69c604fc516445534d36e8063802f5c6a148f93cdc34e5d5a5932` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_prose/cycle01/objection.json` | `7a331fe944fe20018b3087531e131ddcf3f0dd9eee3255e8a239036b0280ad06` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_prose/cycle01/response.json` | `442f65eaa131703c11cc0cbb9f9e55bf69c2a7d0dead6af41757749b17ae2df7` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_prose/cycle01/rival.json` | `e60b3d93f1bf628f637c05a03de32f0cc72441f3ef93a820747325cef0a6df52` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `H005-open-prose-commitments/occurrence-01/artifacts/daily/native/cycle01/answer.json` | `2a1c9b736de2300dbd6caab605d7bd07b7fbfbf5cd172d88ac5725b8bc5ba95e` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `H005-open-prose-commitments/occurrence-01/plan.json` | `99cda29f3c6788d564448f7587c7448a6542d30a9bd5e48dc219925e2cc464c3` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |

## `experiments/diagnostics/C001-contrast-triple/material-occurrence-02.json`

- format detected: JSON mapping (top-level key 'source_pins' -> 64-hex)
- counts: {"MATCH": 8}
- Bases: manifest_dir then sandbox root.

| path | recorded sha256 | verdict | resolution |
|---|---|---|---|
| `docs/sources/FW5-explanatory-construction.md` | `8105925b07db4a17f15c38cbad79aaca16653d94b0503de79756b5ece33ee63a` | MATCH | sandbox_root (docs/sources/FW5-explanatory-construction.md) |
| `experiments/diagnostics/H005-open-prose-commitments/material.json` | `24ca4552016836b488c2644db0f17ba0b20c446e9dc2602a29e5e4b1b756c927` | MATCH | sandbox_root (experiments/diagnostics/H005-open-prose-commitments/material.json) |
| `experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_fcl/cycle01/account.json` | `b8de6a8d579c358cade3296a7e8260a03c6e80269cd0486aae43c134999732e6` | MATCH | sandbox_root (experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_fcl/cycle01/account.json) |
| `experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_fcl/cycle01/objection.json` | `810913b5c31f94a4d697da0e90e74205ac6b7abc7b217d44188852f2562110db` | MATCH | sandbox_root (experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_fcl/cycle01/objection.json) |
| `experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_fcl/cycle01/rival.json` | `b0b15d8d44c7dcd706879a9ced41e3f26a592ec5a25c2a961e01e32ea748e8cd` | MATCH | sandbox_root (experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_fcl/cycle01/rival.json) |
| `experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_prose/cycle01/account.json` | `11bdb5753d4fe7e0bcf2b357cf37afe751e38157e9f1d676f9e32ce63e3f1005` | MATCH | sandbox_root (experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_prose/cycle01/account.json) |
| `experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_prose/cycle01/objection.json` | `7a331fe944fe20018b3087531e131ddcf3f0dd9eee3255e8a239036b0280ad06` | MATCH | sandbox_root (experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_prose/cycle01/objection.json) |
| `experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_prose/cycle01/rival.json` | `e60b3d93f1bf628f637c05a03de32f0cc72441f3ef93a820747325cef0a6df52` | MATCH | sandbox_root (experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_prose/cycle01/rival.json) |

## `experiments/diagnostics/C001-contrast-triple/material.json`

- format detected: JSON mapping (top-level key 'source_pins' -> 64-hex)
- counts: {"MATCH": 8}
- Bases: manifest_dir then sandbox root.

| path | recorded sha256 | verdict | resolution |
|---|---|---|---|
| `docs/sources/FW5-explanatory-construction.md` | `8105925b07db4a17f15c38cbad79aaca16653d94b0503de79756b5ece33ee63a` | MATCH | sandbox_root (docs/sources/FW5-explanatory-construction.md) |
| `experiments/diagnostics/H005-open-prose-commitments/material.json` | `24ca4552016836b488c2644db0f17ba0b20c446e9dc2602a29e5e4b1b756c927` | MATCH | sandbox_root (experiments/diagnostics/H005-open-prose-commitments/material.json) |
| `experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_fcl/cycle01/account.json` | `b8de6a8d579c358cade3296a7e8260a03c6e80269cd0486aae43c134999732e6` | MATCH | sandbox_root (experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_fcl/cycle01/account.json) |
| `experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_fcl/cycle01/objection.json` | `810913b5c31f94a4d697da0e90e74205ac6b7abc7b217d44188852f2562110db` | MATCH | sandbox_root (experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_fcl/cycle01/objection.json) |
| `experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_fcl/cycle01/rival.json` | `b0b15d8d44c7dcd706879a9ced41e3f26a592ec5a25c2a961e01e32ea748e8cd` | MATCH | sandbox_root (experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_fcl/cycle01/rival.json) |
| `experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_prose/cycle01/account.json` | `11bdb5753d4fe7e0bcf2b357cf37afe751e38157e9f1d676f9e32ce63e3f1005` | MATCH | sandbox_root (experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_prose/cycle01/account.json) |
| `experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_prose/cycle01/objection.json` | `7a331fe944fe20018b3087531e131ddcf3f0dd9eee3255e8a239036b0280ad06` | MATCH | sandbox_root (experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_prose/cycle01/objection.json) |
| `experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_prose/cycle01/rival.json` | `e60b3d93f1bf628f637c05a03de32f0cc72441f3ef93a820747325cef0a6df52` | MATCH | sandbox_root (experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_prose/cycle01/rival.json) |

## `experiments/diagnostics/C001-contrast-triple/occurrence-01/material.json`

- format detected: JSON mapping (top-level key 'source_pins' -> 64-hex)
- counts: {"MATCH": 8}
- Bases: manifest_dir then sandbox root.

| path | recorded sha256 | verdict | resolution |
|---|---|---|---|
| `docs/sources/FW5-explanatory-construction.md` | `8105925b07db4a17f15c38cbad79aaca16653d94b0503de79756b5ece33ee63a` | MATCH | sandbox_root (docs/sources/FW5-explanatory-construction.md) |
| `experiments/diagnostics/H005-open-prose-commitments/material.json` | `24ca4552016836b488c2644db0f17ba0b20c446e9dc2602a29e5e4b1b756c927` | MATCH | sandbox_root (experiments/diagnostics/H005-open-prose-commitments/material.json) |
| `experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_fcl/cycle01/account.json` | `b8de6a8d579c358cade3296a7e8260a03c6e80269cd0486aae43c134999732e6` | MATCH | sandbox_root (experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_fcl/cycle01/account.json) |
| `experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_fcl/cycle01/objection.json` | `810913b5c31f94a4d697da0e90e74205ac6b7abc7b217d44188852f2562110db` | MATCH | sandbox_root (experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_fcl/cycle01/objection.json) |
| `experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_fcl/cycle01/rival.json` | `b0b15d8d44c7dcd706879a9ced41e3f26a592ec5a25c2a961e01e32ea748e8cd` | MATCH | sandbox_root (experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_fcl/cycle01/rival.json) |
| `experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_prose/cycle01/account.json` | `11bdb5753d4fe7e0bcf2b357cf37afe751e38157e9f1d676f9e32ce63e3f1005` | MATCH | sandbox_root (experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_prose/cycle01/account.json) |
| `experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_prose/cycle01/objection.json` | `7a331fe944fe20018b3087531e131ddcf3f0dd9eee3255e8a239036b0280ad06` | MATCH | sandbox_root (experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_prose/cycle01/objection.json) |
| `experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_prose/cycle01/rival.json` | `e60b3d93f1bf628f637c05a03de32f0cc72441f3ef93a820747325cef0a6df52` | MATCH | sandbox_root (experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_prose/cycle01/rival.json) |

## `experiments/diagnostics/C001-contrast-triple/occurrence-01/preflight.json`

- format detected: JSON mapping (top-level key 'source_pins_verified' -> 64-hex)
- counts: {"MATCH": 8}
- Bases: manifest_dir then sandbox root.

| path | recorded sha256 | verdict | resolution |
|---|---|---|---|
| `docs/sources/FW5-explanatory-construction.md` | `8105925b07db4a17f15c38cbad79aaca16653d94b0503de79756b5ece33ee63a` | MATCH | sandbox_root (docs/sources/FW5-explanatory-construction.md) |
| `experiments/diagnostics/H005-open-prose-commitments/material.json` | `24ca4552016836b488c2644db0f17ba0b20c446e9dc2602a29e5e4b1b756c927` | MATCH | sandbox_root (experiments/diagnostics/H005-open-prose-commitments/material.json) |
| `experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_fcl/cycle01/account.json` | `b8de6a8d579c358cade3296a7e8260a03c6e80269cd0486aae43c134999732e6` | MATCH | sandbox_root (experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_fcl/cycle01/account.json) |
| `experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_fcl/cycle01/objection.json` | `810913b5c31f94a4d697da0e90e74205ac6b7abc7b217d44188852f2562110db` | MATCH | sandbox_root (experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_fcl/cycle01/objection.json) |
| `experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_fcl/cycle01/rival.json` | `b0b15d8d44c7dcd706879a9ced41e3f26a592ec5a25c2a961e01e32ea748e8cd` | MATCH | sandbox_root (experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_fcl/cycle01/rival.json) |
| `experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_prose/cycle01/account.json` | `11bdb5753d4fe7e0bcf2b357cf37afe751e38157e9f1d676f9e32ce63e3f1005` | MATCH | sandbox_root (experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_prose/cycle01/account.json) |
| `experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_prose/cycle01/objection.json` | `7a331fe944fe20018b3087531e131ddcf3f0dd9eee3255e8a239036b0280ad06` | MATCH | sandbox_root (experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_prose/cycle01/objection.json) |
| `experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_prose/cycle01/rival.json` | `e60b3d93f1bf628f637c05a03de32f0cc72441f3ef93a820747325cef0a6df52` | MATCH | sandbox_root (experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_prose/cycle01/rival.json) |

## `experiments/diagnostics/C001-contrast-triple/occurrence-02/material.json`

- format detected: JSON mapping (top-level key 'source_pins' -> 64-hex)
- counts: {"MATCH": 8}
- Bases: manifest_dir then sandbox root.

| path | recorded sha256 | verdict | resolution |
|---|---|---|---|
| `docs/sources/FW5-explanatory-construction.md` | `8105925b07db4a17f15c38cbad79aaca16653d94b0503de79756b5ece33ee63a` | MATCH | sandbox_root (docs/sources/FW5-explanatory-construction.md) |
| `experiments/diagnostics/H005-open-prose-commitments/material.json` | `24ca4552016836b488c2644db0f17ba0b20c446e9dc2602a29e5e4b1b756c927` | MATCH | sandbox_root (experiments/diagnostics/H005-open-prose-commitments/material.json) |
| `experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_fcl/cycle01/account.json` | `b8de6a8d579c358cade3296a7e8260a03c6e80269cd0486aae43c134999732e6` | MATCH | sandbox_root (experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_fcl/cycle01/account.json) |
| `experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_fcl/cycle01/objection.json` | `810913b5c31f94a4d697da0e90e74205ac6b7abc7b217d44188852f2562110db` | MATCH | sandbox_root (experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_fcl/cycle01/objection.json) |
| `experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_fcl/cycle01/rival.json` | `b0b15d8d44c7dcd706879a9ced41e3f26a592ec5a25c2a961e01e32ea748e8cd` | MATCH | sandbox_root (experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_fcl/cycle01/rival.json) |
| `experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_prose/cycle01/account.json` | `11bdb5753d4fe7e0bcf2b357cf37afe751e38157e9f1d676f9e32ce63e3f1005` | MATCH | sandbox_root (experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_prose/cycle01/account.json) |
| `experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_prose/cycle01/objection.json` | `7a331fe944fe20018b3087531e131ddcf3f0dd9eee3255e8a239036b0280ad06` | MATCH | sandbox_root (experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_prose/cycle01/objection.json) |
| `experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_prose/cycle01/rival.json` | `e60b3d93f1bf628f637c05a03de32f0cc72441f3ef93a820747325cef0a6df52` | MATCH | sandbox_root (experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_prose/cycle01/rival.json) |

## `experiments/diagnostics/C001-contrast-triple/occurrence-02/preflight.json`

- format detected: JSON mapping (top-level key 'source_pins_verified' -> 64-hex)
- counts: {"MATCH": 8}
- Bases: manifest_dir then sandbox root.

| path | recorded sha256 | verdict | resolution |
|---|---|---|---|
| `docs/sources/FW5-explanatory-construction.md` | `8105925b07db4a17f15c38cbad79aaca16653d94b0503de79756b5ece33ee63a` | MATCH | sandbox_root (docs/sources/FW5-explanatory-construction.md) |
| `experiments/diagnostics/H005-open-prose-commitments/material.json` | `24ca4552016836b488c2644db0f17ba0b20c446e9dc2602a29e5e4b1b756c927` | MATCH | sandbox_root (experiments/diagnostics/H005-open-prose-commitments/material.json) |
| `experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_fcl/cycle01/account.json` | `b8de6a8d579c358cade3296a7e8260a03c6e80269cd0486aae43c134999732e6` | MATCH | sandbox_root (experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_fcl/cycle01/account.json) |
| `experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_fcl/cycle01/objection.json` | `810913b5c31f94a4d697da0e90e74205ac6b7abc7b217d44188852f2562110db` | MATCH | sandbox_root (experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_fcl/cycle01/objection.json) |
| `experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_fcl/cycle01/rival.json` | `b0b15d8d44c7dcd706879a9ced41e3f26a592ec5a25c2a961e01e32ea748e8cd` | MATCH | sandbox_root (experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_fcl/cycle01/rival.json) |
| `experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_prose/cycle01/account.json` | `11bdb5753d4fe7e0bcf2b357cf37afe751e38157e9f1d676f9e32ce63e3f1005` | MATCH | sandbox_root (experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_prose/cycle01/account.json) |
| `experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_prose/cycle01/objection.json` | `7a331fe944fe20018b3087531e131ddcf3f0dd9eee3255e8a239036b0280ad06` | MATCH | sandbox_root (experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_prose/cycle01/objection.json) |
| `experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_prose/cycle01/rival.json` | `e60b3d93f1bf628f637c05a03de32f0cc72441f3ef93a820747325cef0a6df52` | MATCH | sandbox_root (experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_prose/cycle01/rival.json) |

## `experiments/diagnostics/F002-fork5-raised-clock/material.json`

- format detected: JSON mapping (top-level key 'source_pins' -> 64-hex)
- counts: {"MATCH": 1}
- Bases: manifest_dir then sandbox root.

| path | recorded sha256 | verdict | resolution |
|---|---|---|---|
| `docs/sources/FW5-explanatory-construction.md` | `8105925b07db4a17f15c38cbad79aaca16653d94b0503de79756b5ece33ee63a` | MATCH | sandbox_root (docs/sources/FW5-explanatory-construction.md) |

## `experiments/diagnostics/F002-fork5-raised-clock/occurrence-01/material.json`

- format detected: JSON mapping (top-level key 'source_pins' -> 64-hex)
- counts: {"MATCH": 1}
- Bases: manifest_dir then sandbox root.

| path | recorded sha256 | verdict | resolution |
|---|---|---|---|
| `docs/sources/FW5-explanatory-construction.md` | `8105925b07db4a17f15c38cbad79aaca16653d94b0503de79756b5ece33ee63a` | MATCH | sandbox_root (docs/sources/FW5-explanatory-construction.md) |

## `experiments/diagnostics/F002-fork5-raised-clock/occurrence-02/material.json`

- format detected: JSON mapping (top-level key 'source_pins' -> 64-hex)
- counts: {"MATCH": 1}
- Bases: manifest_dir then sandbox root.

| path | recorded sha256 | verdict | resolution |
|---|---|---|---|
| `docs/sources/FW5-explanatory-construction.md` | `8105925b07db4a17f15c38cbad79aaca16653d94b0503de79756b5ece33ee63a` | MATCH | sandbox_root (docs/sources/FW5-explanatory-construction.md) |

## `experiments/diagnostics/F002-fork5-raised-clock/occurrence-03/material.json`

- format detected: JSON mapping (top-level key 'source_pins' -> 64-hex)
- counts: {"MATCH": 1}
- Bases: manifest_dir then sandbox root.

| path | recorded sha256 | verdict | resolution |
|---|---|---|---|
| `docs/sources/FW5-explanatory-construction.md` | `8105925b07db4a17f15c38cbad79aaca16653d94b0503de79756b5ece33ee63a` | MATCH | sandbox_root (docs/sources/FW5-explanatory-construction.md) |

## `experiments/diagnostics/H005-open-prose-commitments/material.json`

- format detected: JSON mapping (top-level key 'source_pins' -> 64-hex)
- counts: {"MATCH": 1}
- Bases: manifest_dir then sandbox root.

| path | recorded sha256 | verdict | resolution |
|---|---|---|---|
| `docs/sources/FW5-explanatory-construction.md` | `8105925b07db4a17f15c38cbad79aaca16653d94b0503de79756b5ece33ee63a` | MATCH | sandbox_root (docs/sources/FW5-explanatory-construction.md) |

## `experiments/diagnostics/C001-contrast-triple/occurrence-01/plan.json`

- format detected: JSON pinned fields (material_sha256, helper_sha256, source_pins)
- counts: {"MATCH": 9, "MISSING": 1}

| path | recorded sha256 | verdict | resolution |
|---|---|---|---|
| `material.json` | `94edfe612097441c8a5957c41a8a1140833b89bd155bd9794b60a1bfb8979975` | MATCH | manifest_dir (experiments/diagnostics/C001-contrast-triple/occurrence-01/material.json) |
| `tools/contrast_triple_study.py` | `f5f9dfcadd8bdd769821213b5c09d569480daa20db3a5e8d8d763efd9e08688b` | MISSING -- field helper_sha256; C001 PLAN.md names the driver as tools/contrast_triple_study.py (not copied into this sandbox) | neither base |
| `docs/sources/FW5-explanatory-construction.md` | `8105925b07db4a17f15c38cbad79aaca16653d94b0503de79756b5ece33ee63a` | MATCH | sandbox_root (docs/sources/FW5-explanatory-construction.md) |
| `experiments/diagnostics/H005-open-prose-commitments/material.json` | `24ca4552016836b488c2644db0f17ba0b20c446e9dc2602a29e5e4b1b756c927` | MATCH | sandbox_root (experiments/diagnostics/H005-open-prose-commitments/material.json) |
| `experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_fcl/cycle01/account.json` | `b8de6a8d579c358cade3296a7e8260a03c6e80269cd0486aae43c134999732e6` | MATCH | sandbox_root (experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_fcl/cycle01/account.json) |
| `experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_fcl/cycle01/objection.json` | `810913b5c31f94a4d697da0e90e74205ac6b7abc7b217d44188852f2562110db` | MATCH | sandbox_root (experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_fcl/cycle01/objection.json) |
| `experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_fcl/cycle01/rival.json` | `b0b15d8d44c7dcd706879a9ced41e3f26a592ec5a25c2a961e01e32ea748e8cd` | MATCH | sandbox_root (experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_fcl/cycle01/rival.json) |
| `experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_prose/cycle01/account.json` | `11bdb5753d4fe7e0bcf2b357cf37afe751e38157e9f1d676f9e32ce63e3f1005` | MATCH | sandbox_root (experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_prose/cycle01/account.json) |
| `experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_prose/cycle01/objection.json` | `7a331fe944fe20018b3087531e131ddcf3f0dd9eee3255e8a239036b0280ad06` | MATCH | sandbox_root (experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_prose/cycle01/objection.json) |
| `experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_prose/cycle01/rival.json` | `e60b3d93f1bf628f637c05a03de32f0cc72441f3ef93a820747325cef0a6df52` | MATCH | sandbox_root (experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_prose/cycle01/rival.json) |

## `experiments/diagnostics/C001-contrast-triple/occurrence-02/plan.json`

- format detected: JSON pinned fields (material_sha256, helper_sha256, source_pins)
- counts: {"MATCH": 9, "MISSING": 1}

| path | recorded sha256 | verdict | resolution |
|---|---|---|---|
| `material.json` | `1ba7be081b6fb0c56af7433589ae8bd8591c3a9e697a816d32b0950851874f30` | MATCH | manifest_dir (experiments/diagnostics/C001-contrast-triple/occurrence-02/material.json) |
| `tools/contrast_triple_study.py` | `1857110385da3e2e4740086410ba6f840947dc4d8267527c6c9b86aada80f9cf` | MISSING -- field helper_sha256; C001 PLAN.md names the driver as tools/contrast_triple_study.py (not copied into this sandbox) | neither base |
| `docs/sources/FW5-explanatory-construction.md` | `8105925b07db4a17f15c38cbad79aaca16653d94b0503de79756b5ece33ee63a` | MATCH | sandbox_root (docs/sources/FW5-explanatory-construction.md) |
| `experiments/diagnostics/H005-open-prose-commitments/material.json` | `24ca4552016836b488c2644db0f17ba0b20c446e9dc2602a29e5e4b1b756c927` | MATCH | sandbox_root (experiments/diagnostics/H005-open-prose-commitments/material.json) |
| `experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_fcl/cycle01/account.json` | `b8de6a8d579c358cade3296a7e8260a03c6e80269cd0486aae43c134999732e6` | MATCH | sandbox_root (experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_fcl/cycle01/account.json) |
| `experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_fcl/cycle01/objection.json` | `810913b5c31f94a4d697da0e90e74205ac6b7abc7b217d44188852f2562110db` | MATCH | sandbox_root (experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_fcl/cycle01/objection.json) |
| `experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_fcl/cycle01/rival.json` | `b0b15d8d44c7dcd706879a9ced41e3f26a592ec5a25c2a961e01e32ea748e8cd` | MATCH | sandbox_root (experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_fcl/cycle01/rival.json) |
| `experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_prose/cycle01/account.json` | `11bdb5753d4fe7e0bcf2b357cf37afe751e38157e9f1d676f9e32ce63e3f1005` | MATCH | sandbox_root (experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_prose/cycle01/account.json) |
| `experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_prose/cycle01/objection.json` | `7a331fe944fe20018b3087531e131ddcf3f0dd9eee3255e8a239036b0280ad06` | MATCH | sandbox_root (experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_prose/cycle01/objection.json) |
| `experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_prose/cycle01/rival.json` | `e60b3d93f1bf628f637c05a03de32f0cc72441f3ef93a820747325cef0a6df52` | MATCH | sandbox_root (experiments/diagnostics/H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_prose/cycle01/rival.json) |

## `experiments/diagnostics/F002-fork5-raised-clock/occurrence-01/plan.json`

- format detected: JSON pinned fields (material_sha256, arms_sha256, runner/helper_sha256, source/provider/runtime_pins, manifests)
- counts: {"MATCH": 57}

| path | recorded sha256 | verdict | resolution |
|---|---|---|---|
| `material.json` | `aadea004b4722fb1b4878bc9c46e7ba8ef5883ff6bcbff4aac10020b6b017679` | MATCH | manifest_dir (experiments/diagnostics/F002-fork5-raised-clock/occurrence-01/material.json) |
| `arms.json` | `2a181f80eae29f0716be1fdcae1f67c38df38f096b6cbd7c7a344acbdf013b3b` | MATCH | manifest_dir (experiments/diagnostics/F002-fork5-raised-clock/occurrence-01/arms.json) |
| `tools/multicycle_commitment_study_multi_v3.py` | `ccbb1165fd3bb1d14e6c9247821e9c4e67fbea09a2153339984bd7eaff5cc42e` | MATCH | sandbox_root (tools/multicycle_commitment_study_multi_v3.py) |
| `tools/multicycle_commitment_study_multi_v3.py` | `ccbb1165fd3bb1d14e6c9247821e9c4e67fbea09a2153339984bd7eaff5cc42e` | MATCH | sandbox_root (tools/multicycle_commitment_study_multi_v3.py) |
| `docs/sources/FW5-explanatory-construction.md` | `8105925b07db4a17f15c38cbad79aaca16653d94b0503de79756b5ece33ee63a` | MATCH | sandbox_root (docs/sources/FW5-explanatory-construction.md) |
| `src/minireason/data/endpoints.json` | `03eff16b8f575c113871a1266439874b2622a75d200ecb84a1b79464aa98aee7` | MATCH | sandbox_root (src/minireason/data/endpoints.json) |
| `src/minireason/provider_openai_compat.py` | `cdc4b5711263eae2eebf9eadda3a52ad7b9c1f2320a780adc955bcb3cdaee5db` | MATCH | sandbox_root (src/minireason/provider_openai_compat.py) |
| `src/creib/__init__.py` | `e801c50509ac08640b7e4714982e74eb09568185ee5b82751741e59b5ac95336` | MATCH | sandbox_root (src/creib/__init__.py) |
| `src/creib/canonical.py` | `0ab53379e392de837292b1d10efa0ec87bf647d1880487b2d7aaefaeb35d5077` | MATCH | sandbox_root (src/creib/canonical.py) |
| `src/creib/errors.py` | `301b5e60fb00ae8c1a7b51944d9784843bd9feaa7f3d7fa9349d008c6aeb06c2` | MATCH | sandbox_root (src/creib/errors.py) |
| `src/creib/forge/__init__.py` | `965a348f651d05c23745a18d493aa5cf391ca79a974e00e9309d72f3407b6c22` | MATCH | sandbox_root (src/creib/forge/__init__.py) |
| `src/creib/forge/conformance/__init__.py` | `d388d67fb8eab061be58d0c5cb4e1ec4313a94f58556e13f1fb729fb0eb544b0` | MATCH | sandbox_root (src/creib/forge/conformance/__init__.py) |
| `src/creib/forge/conformance/common.py` | `64f6015c0bb7a895645315ffb1182f818d9c565fe09a029e04f755195ba92477` | MATCH | sandbox_root (src/creib/forge/conformance/common.py) |
| `src/creib/forge/conformance/corpus.py` | `a04a74d2b5ad08a4235fc54746c2bf0cf3812de0fde8ba3b2d947a786f2f141d` | MATCH | sandbox_root (src/creib/forge/conformance/corpus.py) |
| `src/creib/forge/conformance/executor.py` | `98f30e3d65786c3cc1dec1ea1151f1e092e7670ec1a2b93b663dce06b492e242` | MATCH | sandbox_root (src/creib/forge/conformance/executor.py) |
| `src/creib/forge/conformance/families.py` | `3ffa952c0ba50df6f3273d73075bf977ade720d0bd87f3ba375fd66d280dd496` | MATCH | sandbox_root (src/creib/forge/conformance/families.py) |
| `src/creib/forge/conformance/oracle.py` | `dd726af4d4c073ee0881bb27127a4fb5aae8544381831a63202bc2d436fe0a04` | MATCH | sandbox_root (src/creib/forge/conformance/oracle.py) |
| `src/creib/forge/conformance/records.py` | `34be9d7467ca143eafdd1be0713fb711783cae99b8eb58eb7afdad990adb33d4` | MATCH | sandbox_root (src/creib/forge/conformance/records.py) |
| `src/creib/forge/conformance/routing.py` | `0bb2eb0b0f9482283476c6aff45ff0cb03006c92be7b529a85a8dd7c0df256ab` | MATCH | sandbox_root (src/creib/forge/conformance/routing.py) |
| `src/creib/forge/conformance/spec.py` | `2c96e669de1c74c45e07cd28251831b6f9bbbf67aecb140140b1d9f0a9fad3f1` | MATCH | sandbox_root (src/creib/forge/conformance/spec.py) |
| `src/creib/forge/conformance/units.py` | `fcfdae70ec3aedcd7b7c221d6438867c05326cecb8b6d573ae3cfe2327671248` | MATCH | sandbox_root (src/creib/forge/conformance/units.py) |
| `src/creib/forge/mini/__init__.py` | `c9369f7df906e8d9bd7fcb3fc39fdc628568839bfe3eccbcc62c1ddb1bd28fd2` | MATCH | sandbox_root (src/creib/forge/mini/__init__.py) |
| `src/creib/forge/mini/adjudication.py` | `3df75ed262dbc9c8139a746ed2da22803a651bd166c3991ded80c90860432f83` | MATCH | sandbox_root (src/creib/forge/mini/adjudication.py) |
| `src/creib/forge/mini/alarms.py` | `e93348bf62dbd825a5c62c948ca75bff27176e6c131adad6042cf45b9979a941` | MATCH | sandbox_root (src/creib/forge/mini/alarms.py) |
| `src/creib/forge/mini/attention.py` | `596708bda3f493a079299605502cf9a554e33d3b6e3977a884127dece4eaa8c0` | MATCH | sandbox_root (src/creib/forge/mini/attention.py) |
| `src/creib/forge/mini/blindspot.py` | `902e3843210dc8f7c5c7e26a877de5766487ae6a956a99b7054a0b4236335d28` | MATCH | sandbox_root (src/creib/forge/mini/blindspot.py) |
| `src/creib/forge/mini/buildtest.py` | `8f0767bb70839cd27bbdb5214ad190415c3f4cd09c5c19f92f0f6ed06c393c12` | MATCH | sandbox_root (src/creib/forge/mini/buildtest.py) |
| `src/creib/forge/mini/campaign.py` | `9d59a6bae15a269266a0f8588e2dd3dc48e5b0e453e3eafc426b5fb903e95689` | MATCH | sandbox_root (src/creib/forge/mini/campaign.py) |
| `src/creib/forge/mini/common.py` | `03430d7a059ed10f7d57b2186f0d5c348064fa496200958dfc19319cd847cd6a` | MATCH | sandbox_root (src/creib/forge/mini/common.py) |
| `src/creib/forge/mini/compare.py` | `8d59fcbf990e870bae6fe19ce2d87a9e62c8f1a053b84f7162531c563f6c78c1` | MATCH | sandbox_root (src/creib/forge/mini/compare.py) |
| `src/creib/forge/mini/configspace.py` | `8eb336c1f360cd8dd2131769df13a9e97b29349bca4f87d268deba11fb5f6ffd` | MATCH | sandbox_root (src/creib/forge/mini/configspace.py) |
| `src/creib/forge/mini/conformance_kernels.py` | `6705b6c3e297b8f0c6e7b1519de4252a4af43b0545874c388ee513e55b6ddeb4` | MATCH | sandbox_root (src/creib/forge/mini/conformance_kernels.py) |
| `src/creib/forge/mini/evidence.py` | `0737a343afca249ca6c5196d0426add855097a2084c0b82713f8dfef7b8a9095` | MATCH | sandbox_root (src/creib/forge/mini/evidence.py) |
| `src/creib/forge/mini/executor.py` | `2ce5ab3e736759039a7cd0774775a7bfe618c0b27b04204333b65cf33da81400` | MATCH | sandbox_root (src/creib/forge/mini/executor.py) |
| `src/creib/forge/mini/failures.py` | `f424834b15b398367d2a34eb2ad7e3dcb4167a7f6b5a6f7636a556376ca42583` | MATCH | sandbox_root (src/creib/forge/mini/failures.py) |
| `src/creib/forge/mini/formats.py` | `808e8cd6e466ac047dba7d627e90bc1496815c49223e737ce3eea062605d8692` | MATCH | sandbox_root (src/creib/forge/mini/formats.py) |
| `src/creib/forge/mini/kinds.py` | `3c9113dca118146c20ccabe36369925785d7f26bb42db05a88d74779be7e20ff` | MATCH | sandbox_root (src/creib/forge/mini/kinds.py) |
| `src/creib/forge/mini/log.py` | `bc9039ca08a2e6150b5cb75cf485da579718cdac4370b4aa70df260184aca732` | MATCH | sandbox_root (src/creib/forge/mini/log.py) |
| `src/creib/forge/mini/machines.py` | `7ba980561b368e83b92d9afe8cd417b8583836e2fe18c7953d2d40c0b62e14bd` | MATCH | sandbox_root (src/creib/forge/mini/machines.py) |
| `src/creib/forge/mini/manifest.py` | `8c4af62e3d2aac913a4d7248248b6d43b4a757084c4959eaa7285d0e0301f995` | MATCH | sandbox_root (src/creib/forge/mini/manifest.py) |
| `src/creib/forge/mini/openkernels.py` | `8110f805c70074dcf30a6e4f47ae232dbd9b9bacacf652193ced9dc29d0feded` | MATCH | sandbox_root (src/creib/forge/mini/openkernels.py) |
| `src/creib/forge/mini/policy.py` | `e3a8937bdf47a391f6bbdb21592397cedcc3e63f02b3289053480bab6981807f` | MATCH | sandbox_root (src/creib/forge/mini/policy.py) |
| `src/creib/forge/mini/ports.py` | `9ce9cdcc229625b36e901533de8e7498946ca19420b1e1a1b67983ffb8df865e` | MATCH | sandbox_root (src/creib/forge/mini/ports.py) |
| `src/creib/forge/mini/report.py` | `d0786c7be5c710b532062c04f5173374292e9d15acfff0ea81eda9c8cf1be56a` | MATCH | sandbox_root (src/creib/forge/mini/report.py) |
| `src/creib/forge/mini/routing.py` | `fbddc8668ea2a390253de9a752082ef4aa20a6c2bd2ebbf5d7ebcdde50985891` | MATCH | sandbox_root (src/creib/forge/mini/routing.py) |
| `src/creib/forge/mini/runner.py` | `f0f1f5b20e2c50c1a7d1976a63deb6a84a2c5b1ea593918053a52f20e8b7caab` | MATCH | sandbox_root (src/creib/forge/mini/runner.py) |
| `src/creib/forge/mini/signals.py` | `3649ffbefa4ecc24f234d76a74d3c763e2905c7cc9042c1ba2894ad4b88ce630` | MATCH | sandbox_root (src/creib/forge/mini/signals.py) |
| `src/creib/forge/mini/stops.py` | `1981d947ac10ca12b785d3268d8b1e0c18cf3bb3535c3614eaa010d1aeb81bfc` | MATCH | sandbox_root (src/creib/forge/mini/stops.py) |
| `src/creib/forge/mini/usetest.py` | `dbbcd156ef31d770fdc9af677030df0a0fd0ca6c124c8706b958ac269867e41f` | MATCH | sandbox_root (src/creib/forge/mini/usetest.py) |
| `src/creib/forge/mini/windows.py` | `cbd606e5627dd240b4e14d84f45c504713e8059686fdbb74c370458d4c364521` | MATCH | sandbox_root (src/creib/forge/mini/windows.py) |
| `src/creib/forge/schema_validation.py` | `5abbe556e8dfcdb51f8d8a0300beee0fb87acb8a45bb13a59aa4a7794618fa6c` | MATCH | sandbox_root (src/creib/forge/schema_validation.py) |
| `src/creib/strict_json.py` | `62b198a40075bc3addddd676beab0a0b1ed8b841a6cfff51c6970b3172e5eab8` | MATCH | sandbox_root (src/creib/strict_json.py) |
| `src/minireason/provider.py` | `d335fc55879d13cf7ecebf27cd94f5278d45c3905e5bb161708419a14dd35e2e` | MATCH | sandbox_root (src/minireason/provider.py) |
| `tools/multicycle_language_probe.py` | `f107c481b0046255b6df22016688cecb9bea0e89a8199c6d03a582b4aaa55f39` | MATCH | sandbox_root (tools/multicycle_language_probe.py) |
| `manifests/fork5.json` | `8f2d928b2f70298906b17d62e73b41804efa754d845f018d9eb312af7dcb536a` | MATCH | manifest_dir (experiments/diagnostics/F002-fork5-raised-clock/occurrence-01/manifests/fork5.json) |
| `manifests/return6.json` | `bad1f6dc4ddda462f1b3acaa56a9e552eeb98255509cb4bfa3353c2305abb3b5` | MATCH | manifest_dir (experiments/diagnostics/F002-fork5-raised-clock/occurrence-01/manifests/return6.json) |
| `manifests/weave7.json` | `0b8a5f337f754b23fd51721ff287e25347af99648a7d2b00ad73b7baa571c2cb` | MATCH | manifest_dir (experiments/diagnostics/F002-fork5-raised-clock/occurrence-01/manifests/weave7.json) |

## `experiments/diagnostics/F002-fork5-raised-clock/occurrence-02/plan.json`

- format detected: JSON pinned fields (material_sha256, arms_sha256, runner/helper_sha256, source/provider/runtime_pins, manifests)
- counts: {"MATCH": 57}

| path | recorded sha256 | verdict | resolution |
|---|---|---|---|
| `material.json` | `aadea004b4722fb1b4878bc9c46e7ba8ef5883ff6bcbff4aac10020b6b017679` | MATCH | manifest_dir (experiments/diagnostics/F002-fork5-raised-clock/occurrence-02/material.json) |
| `arms.json` | `117d9584d9c559a5be9e7103ffdcd4864740f89a65aca9ee804b5384fb989cef` | MATCH | manifest_dir (experiments/diagnostics/F002-fork5-raised-clock/occurrence-02/arms.json) |
| `tools/multicycle_commitment_study_multi_v3.py` | `ccbb1165fd3bb1d14e6c9247821e9c4e67fbea09a2153339984bd7eaff5cc42e` | MATCH | sandbox_root (tools/multicycle_commitment_study_multi_v3.py) |
| `tools/multicycle_commitment_study_multi_v3.py` | `ccbb1165fd3bb1d14e6c9247821e9c4e67fbea09a2153339984bd7eaff5cc42e` | MATCH | sandbox_root (tools/multicycle_commitment_study_multi_v3.py) |
| `docs/sources/FW5-explanatory-construction.md` | `8105925b07db4a17f15c38cbad79aaca16653d94b0503de79756b5ece33ee63a` | MATCH | sandbox_root (docs/sources/FW5-explanatory-construction.md) |
| `src/minireason/data/endpoints.json` | `03eff16b8f575c113871a1266439874b2622a75d200ecb84a1b79464aa98aee7` | MATCH | sandbox_root (src/minireason/data/endpoints.json) |
| `src/minireason/provider_openai_compat.py` | `cdc4b5711263eae2eebf9eadda3a52ad7b9c1f2320a780adc955bcb3cdaee5db` | MATCH | sandbox_root (src/minireason/provider_openai_compat.py) |
| `src/creib/__init__.py` | `e801c50509ac08640b7e4714982e74eb09568185ee5b82751741e59b5ac95336` | MATCH | sandbox_root (src/creib/__init__.py) |
| `src/creib/canonical.py` | `0ab53379e392de837292b1d10efa0ec87bf647d1880487b2d7aaefaeb35d5077` | MATCH | sandbox_root (src/creib/canonical.py) |
| `src/creib/errors.py` | `301b5e60fb00ae8c1a7b51944d9784843bd9feaa7f3d7fa9349d008c6aeb06c2` | MATCH | sandbox_root (src/creib/errors.py) |
| `src/creib/forge/__init__.py` | `965a348f651d05c23745a18d493aa5cf391ca79a974e00e9309d72f3407b6c22` | MATCH | sandbox_root (src/creib/forge/__init__.py) |
| `src/creib/forge/conformance/__init__.py` | `d388d67fb8eab061be58d0c5cb4e1ec4313a94f58556e13f1fb729fb0eb544b0` | MATCH | sandbox_root (src/creib/forge/conformance/__init__.py) |
| `src/creib/forge/conformance/common.py` | `64f6015c0bb7a895645315ffb1182f818d9c565fe09a029e04f755195ba92477` | MATCH | sandbox_root (src/creib/forge/conformance/common.py) |
| `src/creib/forge/conformance/corpus.py` | `a04a74d2b5ad08a4235fc54746c2bf0cf3812de0fde8ba3b2d947a786f2f141d` | MATCH | sandbox_root (src/creib/forge/conformance/corpus.py) |
| `src/creib/forge/conformance/executor.py` | `98f30e3d65786c3cc1dec1ea1151f1e092e7670ec1a2b93b663dce06b492e242` | MATCH | sandbox_root (src/creib/forge/conformance/executor.py) |
| `src/creib/forge/conformance/families.py` | `3ffa952c0ba50df6f3273d73075bf977ade720d0bd87f3ba375fd66d280dd496` | MATCH | sandbox_root (src/creib/forge/conformance/families.py) |
| `src/creib/forge/conformance/oracle.py` | `dd726af4d4c073ee0881bb27127a4fb5aae8544381831a63202bc2d436fe0a04` | MATCH | sandbox_root (src/creib/forge/conformance/oracle.py) |
| `src/creib/forge/conformance/records.py` | `34be9d7467ca143eafdd1be0713fb711783cae99b8eb58eb7afdad990adb33d4` | MATCH | sandbox_root (src/creib/forge/conformance/records.py) |
| `src/creib/forge/conformance/routing.py` | `0bb2eb0b0f9482283476c6aff45ff0cb03006c92be7b529a85a8dd7c0df256ab` | MATCH | sandbox_root (src/creib/forge/conformance/routing.py) |
| `src/creib/forge/conformance/spec.py` | `2c96e669de1c74c45e07cd28251831b6f9bbbf67aecb140140b1d9f0a9fad3f1` | MATCH | sandbox_root (src/creib/forge/conformance/spec.py) |
| `src/creib/forge/conformance/units.py` | `fcfdae70ec3aedcd7b7c221d6438867c05326cecb8b6d573ae3cfe2327671248` | MATCH | sandbox_root (src/creib/forge/conformance/units.py) |
| `src/creib/forge/mini/__init__.py` | `c9369f7df906e8d9bd7fcb3fc39fdc628568839bfe3eccbcc62c1ddb1bd28fd2` | MATCH | sandbox_root (src/creib/forge/mini/__init__.py) |
| `src/creib/forge/mini/adjudication.py` | `3df75ed262dbc9c8139a746ed2da22803a651bd166c3991ded80c90860432f83` | MATCH | sandbox_root (src/creib/forge/mini/adjudication.py) |
| `src/creib/forge/mini/alarms.py` | `e93348bf62dbd825a5c62c948ca75bff27176e6c131adad6042cf45b9979a941` | MATCH | sandbox_root (src/creib/forge/mini/alarms.py) |
| `src/creib/forge/mini/attention.py` | `596708bda3f493a079299605502cf9a554e33d3b6e3977a884127dece4eaa8c0` | MATCH | sandbox_root (src/creib/forge/mini/attention.py) |
| `src/creib/forge/mini/blindspot.py` | `902e3843210dc8f7c5c7e26a877de5766487ae6a956a99b7054a0b4236335d28` | MATCH | sandbox_root (src/creib/forge/mini/blindspot.py) |
| `src/creib/forge/mini/buildtest.py` | `8f0767bb70839cd27bbdb5214ad190415c3f4cd09c5c19f92f0f6ed06c393c12` | MATCH | sandbox_root (src/creib/forge/mini/buildtest.py) |
| `src/creib/forge/mini/campaign.py` | `9d59a6bae15a269266a0f8588e2dd3dc48e5b0e453e3eafc426b5fb903e95689` | MATCH | sandbox_root (src/creib/forge/mini/campaign.py) |
| `src/creib/forge/mini/common.py` | `03430d7a059ed10f7d57b2186f0d5c348064fa496200958dfc19319cd847cd6a` | MATCH | sandbox_root (src/creib/forge/mini/common.py) |
| `src/creib/forge/mini/compare.py` | `8d59fcbf990e870bae6fe19ce2d87a9e62c8f1a053b84f7162531c563f6c78c1` | MATCH | sandbox_root (src/creib/forge/mini/compare.py) |
| `src/creib/forge/mini/configspace.py` | `8eb336c1f360cd8dd2131769df13a9e97b29349bca4f87d268deba11fb5f6ffd` | MATCH | sandbox_root (src/creib/forge/mini/configspace.py) |
| `src/creib/forge/mini/conformance_kernels.py` | `6705b6c3e297b8f0c6e7b1519de4252a4af43b0545874c388ee513e55b6ddeb4` | MATCH | sandbox_root (src/creib/forge/mini/conformance_kernels.py) |
| `src/creib/forge/mini/evidence.py` | `0737a343afca249ca6c5196d0426add855097a2084c0b82713f8dfef7b8a9095` | MATCH | sandbox_root (src/creib/forge/mini/evidence.py) |
| `src/creib/forge/mini/executor.py` | `2ce5ab3e736759039a7cd0774775a7bfe618c0b27b04204333b65cf33da81400` | MATCH | sandbox_root (src/creib/forge/mini/executor.py) |
| `src/creib/forge/mini/failures.py` | `f424834b15b398367d2a34eb2ad7e3dcb4167a7f6b5a6f7636a556376ca42583` | MATCH | sandbox_root (src/creib/forge/mini/failures.py) |
| `src/creib/forge/mini/formats.py` | `808e8cd6e466ac047dba7d627e90bc1496815c49223e737ce3eea062605d8692` | MATCH | sandbox_root (src/creib/forge/mini/formats.py) |
| `src/creib/forge/mini/kinds.py` | `3c9113dca118146c20ccabe36369925785d7f26bb42db05a88d74779be7e20ff` | MATCH | sandbox_root (src/creib/forge/mini/kinds.py) |
| `src/creib/forge/mini/log.py` | `bc9039ca08a2e6150b5cb75cf485da579718cdac4370b4aa70df260184aca732` | MATCH | sandbox_root (src/creib/forge/mini/log.py) |
| `src/creib/forge/mini/machines.py` | `7ba980561b368e83b92d9afe8cd417b8583836e2fe18c7953d2d40c0b62e14bd` | MATCH | sandbox_root (src/creib/forge/mini/machines.py) |
| `src/creib/forge/mini/manifest.py` | `8c4af62e3d2aac913a4d7248248b6d43b4a757084c4959eaa7285d0e0301f995` | MATCH | sandbox_root (src/creib/forge/mini/manifest.py) |
| `src/creib/forge/mini/openkernels.py` | `8110f805c70074dcf30a6e4f47ae232dbd9b9bacacf652193ced9dc29d0feded` | MATCH | sandbox_root (src/creib/forge/mini/openkernels.py) |
| `src/creib/forge/mini/policy.py` | `e3a8937bdf47a391f6bbdb21592397cedcc3e63f02b3289053480bab6981807f` | MATCH | sandbox_root (src/creib/forge/mini/policy.py) |
| `src/creib/forge/mini/ports.py` | `9ce9cdcc229625b36e901533de8e7498946ca19420b1e1a1b67983ffb8df865e` | MATCH | sandbox_root (src/creib/forge/mini/ports.py) |
| `src/creib/forge/mini/report.py` | `d0786c7be5c710b532062c04f5173374292e9d15acfff0ea81eda9c8cf1be56a` | MATCH | sandbox_root (src/creib/forge/mini/report.py) |
| `src/creib/forge/mini/routing.py` | `fbddc8668ea2a390253de9a752082ef4aa20a6c2bd2ebbf5d7ebcdde50985891` | MATCH | sandbox_root (src/creib/forge/mini/routing.py) |
| `src/creib/forge/mini/runner.py` | `f0f1f5b20e2c50c1a7d1976a63deb6a84a2c5b1ea593918053a52f20e8b7caab` | MATCH | sandbox_root (src/creib/forge/mini/runner.py) |
| `src/creib/forge/mini/signals.py` | `3649ffbefa4ecc24f234d76a74d3c763e2905c7cc9042c1ba2894ad4b88ce630` | MATCH | sandbox_root (src/creib/forge/mini/signals.py) |
| `src/creib/forge/mini/stops.py` | `1981d947ac10ca12b785d3268d8b1e0c18cf3bb3535c3614eaa010d1aeb81bfc` | MATCH | sandbox_root (src/creib/forge/mini/stops.py) |
| `src/creib/forge/mini/usetest.py` | `dbbcd156ef31d770fdc9af677030df0a0fd0ca6c124c8706b958ac269867e41f` | MATCH | sandbox_root (src/creib/forge/mini/usetest.py) |
| `src/creib/forge/mini/windows.py` | `cbd606e5627dd240b4e14d84f45c504713e8059686fdbb74c370458d4c364521` | MATCH | sandbox_root (src/creib/forge/mini/windows.py) |
| `src/creib/forge/schema_validation.py` | `5abbe556e8dfcdb51f8d8a0300beee0fb87acb8a45bb13a59aa4a7794618fa6c` | MATCH | sandbox_root (src/creib/forge/schema_validation.py) |
| `src/creib/strict_json.py` | `62b198a40075bc3addddd676beab0a0b1ed8b841a6cfff51c6970b3172e5eab8` | MATCH | sandbox_root (src/creib/strict_json.py) |
| `src/minireason/provider.py` | `d335fc55879d13cf7ecebf27cd94f5278d45c3905e5bb161708419a14dd35e2e` | MATCH | sandbox_root (src/minireason/provider.py) |
| `tools/multicycle_language_probe.py` | `f107c481b0046255b6df22016688cecb9bea0e89a8199c6d03a582b4aaa55f39` | MATCH | sandbox_root (tools/multicycle_language_probe.py) |
| `manifests/fork5.json` | `8f2d928b2f70298906b17d62e73b41804efa754d845f018d9eb312af7dcb536a` | MATCH | manifest_dir (experiments/diagnostics/F002-fork5-raised-clock/occurrence-02/manifests/fork5.json) |
| `manifests/return6.json` | `bad1f6dc4ddda462f1b3acaa56a9e552eeb98255509cb4bfa3353c2305abb3b5` | MATCH | manifest_dir (experiments/diagnostics/F002-fork5-raised-clock/occurrence-02/manifests/return6.json) |
| `manifests/weave7.json` | `0b8a5f337f754b23fd51721ff287e25347af99648a7d2b00ad73b7baa571c2cb` | MATCH | manifest_dir (experiments/diagnostics/F002-fork5-raised-clock/occurrence-02/manifests/weave7.json) |

## `experiments/diagnostics/F002-fork5-raised-clock/occurrence-03/plan.json`

- format detected: JSON pinned fields (material_sha256, arms_sha256, runner/helper_sha256, source/provider/runtime_pins, manifests)
- counts: {"MATCH": 57}

| path | recorded sha256 | verdict | resolution |
|---|---|---|---|
| `material.json` | `aadea004b4722fb1b4878bc9c46e7ba8ef5883ff6bcbff4aac10020b6b017679` | MATCH | manifest_dir (experiments/diagnostics/F002-fork5-raised-clock/occurrence-03/material.json) |
| `arms.json` | `2a181f80eae29f0716be1fdcae1f67c38df38f096b6cbd7c7a344acbdf013b3b` | MATCH | manifest_dir (experiments/diagnostics/F002-fork5-raised-clock/occurrence-03/arms.json) |
| `tools/multicycle_commitment_study_multi_v3.py` | `ccbb1165fd3bb1d14e6c9247821e9c4e67fbea09a2153339984bd7eaff5cc42e` | MATCH | sandbox_root (tools/multicycle_commitment_study_multi_v3.py) |
| `tools/multicycle_commitment_study_multi_v3.py` | `ccbb1165fd3bb1d14e6c9247821e9c4e67fbea09a2153339984bd7eaff5cc42e` | MATCH | sandbox_root (tools/multicycle_commitment_study_multi_v3.py) |
| `docs/sources/FW5-explanatory-construction.md` | `8105925b07db4a17f15c38cbad79aaca16653d94b0503de79756b5ece33ee63a` | MATCH | sandbox_root (docs/sources/FW5-explanatory-construction.md) |
| `src/minireason/data/endpoints.json` | `03eff16b8f575c113871a1266439874b2622a75d200ecb84a1b79464aa98aee7` | MATCH | sandbox_root (src/minireason/data/endpoints.json) |
| `src/minireason/provider_openai_compat.py` | `cdc4b5711263eae2eebf9eadda3a52ad7b9c1f2320a780adc955bcb3cdaee5db` | MATCH | sandbox_root (src/minireason/provider_openai_compat.py) |
| `src/creib/__init__.py` | `e801c50509ac08640b7e4714982e74eb09568185ee5b82751741e59b5ac95336` | MATCH | sandbox_root (src/creib/__init__.py) |
| `src/creib/canonical.py` | `0ab53379e392de837292b1d10efa0ec87bf647d1880487b2d7aaefaeb35d5077` | MATCH | sandbox_root (src/creib/canonical.py) |
| `src/creib/errors.py` | `301b5e60fb00ae8c1a7b51944d9784843bd9feaa7f3d7fa9349d008c6aeb06c2` | MATCH | sandbox_root (src/creib/errors.py) |
| `src/creib/forge/__init__.py` | `965a348f651d05c23745a18d493aa5cf391ca79a974e00e9309d72f3407b6c22` | MATCH | sandbox_root (src/creib/forge/__init__.py) |
| `src/creib/forge/conformance/__init__.py` | `d388d67fb8eab061be58d0c5cb4e1ec4313a94f58556e13f1fb729fb0eb544b0` | MATCH | sandbox_root (src/creib/forge/conformance/__init__.py) |
| `src/creib/forge/conformance/common.py` | `64f6015c0bb7a895645315ffb1182f818d9c565fe09a029e04f755195ba92477` | MATCH | sandbox_root (src/creib/forge/conformance/common.py) |
| `src/creib/forge/conformance/corpus.py` | `a04a74d2b5ad08a4235fc54746c2bf0cf3812de0fde8ba3b2d947a786f2f141d` | MATCH | sandbox_root (src/creib/forge/conformance/corpus.py) |
| `src/creib/forge/conformance/executor.py` | `98f30e3d65786c3cc1dec1ea1151f1e092e7670ec1a2b93b663dce06b492e242` | MATCH | sandbox_root (src/creib/forge/conformance/executor.py) |
| `src/creib/forge/conformance/families.py` | `3ffa952c0ba50df6f3273d73075bf977ade720d0bd87f3ba375fd66d280dd496` | MATCH | sandbox_root (src/creib/forge/conformance/families.py) |
| `src/creib/forge/conformance/oracle.py` | `dd726af4d4c073ee0881bb27127a4fb5aae8544381831a63202bc2d436fe0a04` | MATCH | sandbox_root (src/creib/forge/conformance/oracle.py) |
| `src/creib/forge/conformance/records.py` | `34be9d7467ca143eafdd1be0713fb711783cae99b8eb58eb7afdad990adb33d4` | MATCH | sandbox_root (src/creib/forge/conformance/records.py) |
| `src/creib/forge/conformance/routing.py` | `0bb2eb0b0f9482283476c6aff45ff0cb03006c92be7b529a85a8dd7c0df256ab` | MATCH | sandbox_root (src/creib/forge/conformance/routing.py) |
| `src/creib/forge/conformance/spec.py` | `2c96e669de1c74c45e07cd28251831b6f9bbbf67aecb140140b1d9f0a9fad3f1` | MATCH | sandbox_root (src/creib/forge/conformance/spec.py) |
| `src/creib/forge/conformance/units.py` | `fcfdae70ec3aedcd7b7c221d6438867c05326cecb8b6d573ae3cfe2327671248` | MATCH | sandbox_root (src/creib/forge/conformance/units.py) |
| `src/creib/forge/mini/__init__.py` | `c9369f7df906e8d9bd7fcb3fc39fdc628568839bfe3eccbcc62c1ddb1bd28fd2` | MATCH | sandbox_root (src/creib/forge/mini/__init__.py) |
| `src/creib/forge/mini/adjudication.py` | `3df75ed262dbc9c8139a746ed2da22803a651bd166c3991ded80c90860432f83` | MATCH | sandbox_root (src/creib/forge/mini/adjudication.py) |
| `src/creib/forge/mini/alarms.py` | `e93348bf62dbd825a5c62c948ca75bff27176e6c131adad6042cf45b9979a941` | MATCH | sandbox_root (src/creib/forge/mini/alarms.py) |
| `src/creib/forge/mini/attention.py` | `596708bda3f493a079299605502cf9a554e33d3b6e3977a884127dece4eaa8c0` | MATCH | sandbox_root (src/creib/forge/mini/attention.py) |
| `src/creib/forge/mini/blindspot.py` | `902e3843210dc8f7c5c7e26a877de5766487ae6a956a99b7054a0b4236335d28` | MATCH | sandbox_root (src/creib/forge/mini/blindspot.py) |
| `src/creib/forge/mini/buildtest.py` | `8f0767bb70839cd27bbdb5214ad190415c3f4cd09c5c19f92f0f6ed06c393c12` | MATCH | sandbox_root (src/creib/forge/mini/buildtest.py) |
| `src/creib/forge/mini/campaign.py` | `9d59a6bae15a269266a0f8588e2dd3dc48e5b0e453e3eafc426b5fb903e95689` | MATCH | sandbox_root (src/creib/forge/mini/campaign.py) |
| `src/creib/forge/mini/common.py` | `03430d7a059ed10f7d57b2186f0d5c348064fa496200958dfc19319cd847cd6a` | MATCH | sandbox_root (src/creib/forge/mini/common.py) |
| `src/creib/forge/mini/compare.py` | `8d59fcbf990e870bae6fe19ce2d87a9e62c8f1a053b84f7162531c563f6c78c1` | MATCH | sandbox_root (src/creib/forge/mini/compare.py) |
| `src/creib/forge/mini/configspace.py` | `8eb336c1f360cd8dd2131769df13a9e97b29349bca4f87d268deba11fb5f6ffd` | MATCH | sandbox_root (src/creib/forge/mini/configspace.py) |
| `src/creib/forge/mini/conformance_kernels.py` | `6705b6c3e297b8f0c6e7b1519de4252a4af43b0545874c388ee513e55b6ddeb4` | MATCH | sandbox_root (src/creib/forge/mini/conformance_kernels.py) |
| `src/creib/forge/mini/evidence.py` | `0737a343afca249ca6c5196d0426add855097a2084c0b82713f8dfef7b8a9095` | MATCH | sandbox_root (src/creib/forge/mini/evidence.py) |
| `src/creib/forge/mini/executor.py` | `2ce5ab3e736759039a7cd0774775a7bfe618c0b27b04204333b65cf33da81400` | MATCH | sandbox_root (src/creib/forge/mini/executor.py) |
| `src/creib/forge/mini/failures.py` | `f424834b15b398367d2a34eb2ad7e3dcb4167a7f6b5a6f7636a556376ca42583` | MATCH | sandbox_root (src/creib/forge/mini/failures.py) |
| `src/creib/forge/mini/formats.py` | `808e8cd6e466ac047dba7d627e90bc1496815c49223e737ce3eea062605d8692` | MATCH | sandbox_root (src/creib/forge/mini/formats.py) |
| `src/creib/forge/mini/kinds.py` | `3c9113dca118146c20ccabe36369925785d7f26bb42db05a88d74779be7e20ff` | MATCH | sandbox_root (src/creib/forge/mini/kinds.py) |
| `src/creib/forge/mini/log.py` | `bc9039ca08a2e6150b5cb75cf485da579718cdac4370b4aa70df260184aca732` | MATCH | sandbox_root (src/creib/forge/mini/log.py) |
| `src/creib/forge/mini/machines.py` | `7ba980561b368e83b92d9afe8cd417b8583836e2fe18c7953d2d40c0b62e14bd` | MATCH | sandbox_root (src/creib/forge/mini/machines.py) |
| `src/creib/forge/mini/manifest.py` | `8c4af62e3d2aac913a4d7248248b6d43b4a757084c4959eaa7285d0e0301f995` | MATCH | sandbox_root (src/creib/forge/mini/manifest.py) |
| `src/creib/forge/mini/openkernels.py` | `8110f805c70074dcf30a6e4f47ae232dbd9b9bacacf652193ced9dc29d0feded` | MATCH | sandbox_root (src/creib/forge/mini/openkernels.py) |
| `src/creib/forge/mini/policy.py` | `e3a8937bdf47a391f6bbdb21592397cedcc3e63f02b3289053480bab6981807f` | MATCH | sandbox_root (src/creib/forge/mini/policy.py) |
| `src/creib/forge/mini/ports.py` | `9ce9cdcc229625b36e901533de8e7498946ca19420b1e1a1b67983ffb8df865e` | MATCH | sandbox_root (src/creib/forge/mini/ports.py) |
| `src/creib/forge/mini/report.py` | `d0786c7be5c710b532062c04f5173374292e9d15acfff0ea81eda9c8cf1be56a` | MATCH | sandbox_root (src/creib/forge/mini/report.py) |
| `src/creib/forge/mini/routing.py` | `fbddc8668ea2a390253de9a752082ef4aa20a6c2bd2ebbf5d7ebcdde50985891` | MATCH | sandbox_root (src/creib/forge/mini/routing.py) |
| `src/creib/forge/mini/runner.py` | `f0f1f5b20e2c50c1a7d1976a63deb6a84a2c5b1ea593918053a52f20e8b7caab` | MATCH | sandbox_root (src/creib/forge/mini/runner.py) |
| `src/creib/forge/mini/signals.py` | `3649ffbefa4ecc24f234d76a74d3c763e2905c7cc9042c1ba2894ad4b88ce630` | MATCH | sandbox_root (src/creib/forge/mini/signals.py) |
| `src/creib/forge/mini/stops.py` | `1981d947ac10ca12b785d3268d8b1e0c18cf3bb3535c3614eaa010d1aeb81bfc` | MATCH | sandbox_root (src/creib/forge/mini/stops.py) |
| `src/creib/forge/mini/usetest.py` | `dbbcd156ef31d770fdc9af677030df0a0fd0ca6c124c8706b958ac269867e41f` | MATCH | sandbox_root (src/creib/forge/mini/usetest.py) |
| `src/creib/forge/mini/windows.py` | `cbd606e5627dd240b4e14d84f45c504713e8059686fdbb74c370458d4c364521` | MATCH | sandbox_root (src/creib/forge/mini/windows.py) |
| `src/creib/forge/schema_validation.py` | `5abbe556e8dfcdb51f8d8a0300beee0fb87acb8a45bb13a59aa4a7794618fa6c` | MATCH | sandbox_root (src/creib/forge/schema_validation.py) |
| `src/creib/strict_json.py` | `62b198a40075bc3addddd676beab0a0b1ed8b841a6cfff51c6970b3172e5eab8` | MATCH | sandbox_root (src/creib/strict_json.py) |
| `src/minireason/provider.py` | `d335fc55879d13cf7ecebf27cd94f5278d45c3905e5bb161708419a14dd35e2e` | MATCH | sandbox_root (src/minireason/provider.py) |
| `tools/multicycle_language_probe.py` | `f107c481b0046255b6df22016688cecb9bea0e89a8199c6d03a582b4aaa55f39` | MATCH | sandbox_root (tools/multicycle_language_probe.py) |
| `manifests/fork5.json` | `8f2d928b2f70298906b17d62e73b41804efa754d845f018d9eb312af7dcb536a` | MATCH | manifest_dir (experiments/diagnostics/F002-fork5-raised-clock/occurrence-03/manifests/fork5.json) |
| `manifests/return6.json` | `bad1f6dc4ddda462f1b3acaa56a9e552eeb98255509cb4bfa3353c2305abb3b5` | MATCH | manifest_dir (experiments/diagnostics/F002-fork5-raised-clock/occurrence-03/manifests/return6.json) |
| `manifests/weave7.json` | `0b8a5f337f754b23fd51721ff287e25347af99648a7d2b00ad73b7baa571c2cb` | MATCH | manifest_dir (experiments/diagnostics/F002-fork5-raised-clock/occurrence-03/manifests/weave7.json) |

## `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md`

- format detected: markdown table rows `| path | sha256 |`
- counts: {"MISSING": 122}

| path | recorded sha256 | verdict | resolution |
|---|---|---|---|
| `F001-fork5-multifamily/occurrence-01/arms.json` | `5165c89e2179b4fa82c8b7f2529063c0ded25c9b4c0466107be17c98e0fc5aa1` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-01/artifacts/daily/bare/cycle01/answer.json` | `44e1de8ffb17a5a986483e84209f3b988c69a0c83f1df63f25f20e9ac0018dbb` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-01/artifacts/daily/mini_fcl/cycle01/account.json` | `61016c4955d08a97f30d21c69d8cd8d7c0af0ba16b5fe61a7aa162bba0bcd6f0` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-01/artifacts/daily/mini_fcl/cycle01/carry.json` | `ece57747fc6f573aedc0695d22c0492864c820b753f3fe82ee47c1597292e587` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-01/artifacts/daily/mini_fcl/cycle01/objection.json` | `837afc39f263be01471367b9c4bae44ce248960e4ebfe48b7e9436cd0d7c5bdf` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-01/artifacts/daily/mini_fcl/cycle01/response.json` | `2fb7525c7ed516096e6c19db528c12372d7edbaf9c9a68dfa7c1bb9f0eeaa3f5` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-01/artifacts/daily/mini_fcl/cycle01/rival.json` | `d2731fe88de3f53a3656f983c75814f8168281edc218cf7fec7c3db7758ebd69` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-01/artifacts/daily/mini_prose/cycle01/account.json` | `6c31a55824b06279f5e11564b47d3688f44b4d32a449708a79a33e979f89c8df` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-01/artifacts/daily/mini_prose/cycle01/carry.json` | `29d1d9caa299708e852e694aaec603e12b80592d1e5af84222685d48bd3b8b3f` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-01/artifacts/daily/mini_prose/cycle01/objection.json` | `16b96dba473d9469946e99533396add0b80118f8cf4eb543862f8140c9da1288` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-01/artifacts/daily/mini_prose/cycle01/response.json` | `9cafb0718055c4c02209978851b3e3dc73274e96f2be2781cb63a92febb970ba` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-01/artifacts/daily/mini_prose/cycle01/rival.json` | `115093ff57135d44019e0bb7a6ee764562c0f7a7ea0677e06f8691e16fd37297` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-01/artifacts/daily/native/cycle01/answer.json` | `c584244b1b1b3e5118367f6892a7a65a1dafdeda4cd80db93fe2eca8bf5bd4d3` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-01/plan.json` | `6992988f7c70c6af9e1df91c5bd30c676ed2bbd1f4cf23ff707489e82b6f7d55` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-02/arms.json` | `32019959b2506763d8061ee033d274857c7593018214f26bb1cb804795588750` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-02/artifacts/daily/bare/cycle01/answer.json` | `f9fccbf0829879365eb9e2590482cd77b1dc21dbb9a89be7446d5e4ce1496843` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-02/artifacts/daily/mini_fcl/cycle01/account.json` | `d42bb4fe95dd750a782409ea27b0967442f841a050b54e9f103a6e314d255931` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-02/artifacts/daily/mini_fcl/cycle01/carry.json` | `b65a344869c39a49b162ebdb68790d44faa606865cef4b62111ee2ac22a31ba0` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-02/artifacts/daily/mini_fcl/cycle01/objection.json` | `de866de7fdbadea24291ecfa6a74027fa6d6b95620005e38752612c3a20cbb09` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-02/artifacts/daily/mini_fcl/cycle01/response.json` | `213d67082128cd0e13fda2b39c45b6f2aa67e863f57a9f0e2b388ecffdeb2d4b` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-02/artifacts/daily/mini_fcl/cycle01/rival.json` | `0ada966d21486a6952db0eeeff99d233246021acc53248eaa7c5f5e651e5d515` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-02/artifacts/daily/mini_prose/cycle01/account.json` | `f464fa0feb6c4cf9d08b43ec65cd7874bf1f07d856690a1bda83b3fb9c265f57` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-02/artifacts/daily/mini_prose/cycle01/carry.json` | `7f9fabdf5fa0a7b12f3545eff8744d3031c2febc55a9289ec0a0a415aadb31cf` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-02/artifacts/daily/mini_prose/cycle01/objection.json` | `02c4d8e4fea7d1c605754c7755eadf6507040dc5961b17c89fca8d9de722556f` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-02/artifacts/daily/mini_prose/cycle01/response.json` | `ba8a3d41440cce94aee5d864bb7e68380f49ab8f91abd4b6f05b0e280b83cf66` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-02/artifacts/daily/mini_prose/cycle01/rival.json` | `84c2c602b38c22ce1f3d3457bd1dac50617f976a088c8d5f5eea065d05cda66f` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-02/plan.json` | `6609038beaa616d7c27467470dde0cb842071c9ec7006530c3f49ffab13ee58e` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-03/arms.json` | `22cd4ea2542f621b68751345cf135e38210b5d654d937efad281c2887dc6dd51` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-03/artifacts/daily/bare/cycle01/answer.json` | `1a0cfda179d837a427ad9e8091c7e658fad96abe9ae98f95d0a8f81c74915d8b` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-03/artifacts/daily/mini_fcl/cycle01/account.json` | `68a181ab635859cb21020a95e9700bd056509d44160b42fa4b8c8cfbe417d55a` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-03/artifacts/daily/mini_fcl/cycle01/carry.json` | `60f477a1782e760594c15b58ee4386121adb0bd3564d4e5e4d578ca890cdb486` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-03/artifacts/daily/mini_fcl/cycle01/objection.json` | `905de875e846cd93b026129e0fa7e41c18a4db0a5e9ccb55192a7518b8746edc` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-03/artifacts/daily/mini_fcl/cycle01/response.json` | `70e09e1f5bdc914237e2a46b33aed70c19277c0ee243f7a2a4e6fce16008c4f4` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-03/artifacts/daily/mini_fcl/cycle01/rival.json` | `4eaf7b12319d74d5a28c22e73a7f13c0248709f9da767fb8832486b0396e4f47` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-03/artifacts/daily/mini_prose/cycle01/account.json` | `9dd02cbe27cab440bd2028bec2ad7a5bb2cdae2ce8589b93d185a670148cc308` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-03/artifacts/daily/mini_prose/cycle01/carry.json` | `cece31dd208559941fd2a735da8e80b11bcb3e66947430bd3a5dac0d524a2e76` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-03/artifacts/daily/mini_prose/cycle01/objection.json` | `5f8b6117dde25213c9e334d9d8f62d1d7cbc93bea1ddf9017f4813e5538c1ad7` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-03/artifacts/daily/mini_prose/cycle01/response.json` | `f89710455a6ee4f231c0db223a63678c2bf18f28d4b80a4916aee596413003dd` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-03/artifacts/daily/mini_prose/cycle01/rival.json` | `ad617038191076557d0caa100fe1c2c808252c72aab8751c11bcde744a2edded` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-03/plan.json` | `5d3d2cd0a6d342f9ef8ea11a4c7e3b26b6ec311af4c835c9cb682a847be86e2d` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-04/arms.json` | `ca5bdcc8a58b6484ca9d5766690a157443884ac374fbc1a921af3b3ed4d5c984` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-04/artifacts/daily/bare/cycle01/answer.json` | `caf27324cf87d3e3f7a5999d35c6035545c5cb0c88297c062dbb474fd9ebb242` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-04/artifacts/daily/mini_fcl/cycle01/account.json` | `f34da0cb4b9a31c5b4072596258b04eb94849fd08380b1899a5cad1e14bc09a6` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-04/artifacts/daily/mini_prose/cycle01/account.json` | `561294d73c77e7778ab70f3fe86033bbda54b3c34b58d31eb401f1928031725a` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-04/artifacts/daily/mini_prose/cycle01/objection.json` | `2896cf1b3bda4e1423c637c05c4197003982e162c63ca06d005cbd81f3675354` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-04/artifacts/daily/mini_prose/cycle01/rival.json` | `09e9828de01550b78b05073041beb53ba1088c6f9708848882740576a60002f5` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-04/plan.json` | `7d06bdaae719af403cf1df715cee213e87ca310ebaf71a85a92ab5f9ba9ffc1f` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-05/arms.json` | `f06eebde55d74c33b4ad2707b0582453db73d9320b21e34e9e9375427f0cb35c` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-05/artifacts/daily/bare/cycle01/answer.json` | `5f8649f563fa59dba1f9e507130ee0470ba3afe7e22127921fe641ccba0d95df` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-05/artifacts/daily/mini_fcl/cycle01/account.json` | `199fdfce722f92d5341a2b28b03c95856bced948fe10704985fd6caeff313ebf` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-05/artifacts/daily/mini_fcl/cycle01/objection.json` | `68257ce650e37d87cc23869e7793e10282aba93bc37c59e8d9d4922b2747ba9e` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-05/artifacts/daily/mini_fcl/cycle01/rival.json` | `7fa39b7cb4264888b550828e662b0127e6b97f0fc62bd704c06cc7fc40795741` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-05/artifacts/daily/mini_prose/cycle01/account.json` | `399e611599467995f5a3fa41c772b23ddc49be66f362aaf9181cdf4285ed4ce3` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-05/artifacts/daily/mini_prose/cycle01/objection.json` | `3796177d5680ea1913ee8eb939fcbc7a755e97204a99926735161dc5e879a53c` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-05/artifacts/daily/mini_prose/cycle01/response.json` | `3066b5652c09dab4fde54829d2dcf7c36f181058f8b62fd3402ab2d7ba3e194b` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-05/artifacts/daily/mini_prose/cycle01/rival.json` | `8872042f76fa0e877e0369decd8b48ec89f38b54a3a05e54907e895352463950` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-05/plan.json` | `4a756b51d9ceb45b787b9741b025104caa5e8e2627bea0d94c85e48622956342` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-06/arms.json` | `80f846ad4e67c2d7ef6eae6ee6a008ef39ef1d806fac581c1e5e0838f43d0b4c` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-06/artifacts/daily/bare/cycle01/answer.json` | `705882f310a357815e8aa76b776b8bd0049cc5776a133f81451189d58b1119c3` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-06/artifacts/daily/mini_fcl/cycle01/account.json` | `a4d341fde4cc7ba67574b09e0720ba91aea9ec131f1189ae7a9f792651be9067` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-06/artifacts/daily/mini_fcl/cycle01/carry.json` | `fbb91d32d6173ccacdfc1f6bcb46cfde3e4eacfa895e4be54a4ebb3302015c7d` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-06/artifacts/daily/mini_fcl/cycle01/objection.json` | `1be20731a470709231d4fdff9cf062c3a1130c6fb0c2bea350346fc541e2753f` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-06/artifacts/daily/mini_fcl/cycle01/response.json` | `25f2997e8bd6433a485fffa01f76e8dcda794c29959e4f802429cf991b158e58` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-06/artifacts/daily/mini_fcl/cycle01/rival.json` | `043882fc7b920ac73f460f4309c7e19dcc8083551d961521c7955a7f1174062f` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-06/artifacts/daily/mini_prose/cycle01/account.json` | `3d7fc6ef6c8d4700a3ddb544651591f9b3624e33ddd405377c9a77d269fa97cd` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-06/artifacts/daily/mini_prose/cycle01/carry.json` | `e38ff0b8ca674e274e84b1df7e3117192777abeb815fadb840b71f88a102a586` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-06/artifacts/daily/mini_prose/cycle01/objection.json` | `314e3fb2551beb9682d90a2f9da1aee903613b8d6de18c91f1e994e912c7d23e` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-06/artifacts/daily/mini_prose/cycle01/response.json` | `c3e46a926e4a1f7e32ad4cd8b904b7278c5e5c42dfb44c9e97eb9692c00064f4` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-06/artifacts/daily/mini_prose/cycle01/rival.json` | `8ce7b1c63f0c77c9a5283a1c219610fdcd1ef487fcdec81b793269b01406a4ea` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-06/plan.json` | `ee565d3fb40bf4c96c555dbb7994c09ce6e1899011d9b53c8b7bd8632f11e8ad` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-07/arms.json` | `16742fd92972a2d3c80b0d061d0eba51c74a644c761ead984d884eaa46a69199` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-07/artifacts/daily/bare/cycle01/answer.json` | `5d22c22df477cba40210537253c905b6d962b9d0a7c8c93589f3d8add529c64e` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-07/artifacts/daily/mini_fcl/cycle01/account.json` | `47f1448f11a7fe22af3d5ce14e965390b2ca6e0aff867962319f68acec12ee71` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-07/artifacts/daily/mini_fcl/cycle01/rival.json` | `2e6699a1fb6a43d2e024223f2a1b6fc0ac52292e221b9344648f12f42bccf64b` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-07/artifacts/daily/mini_prose/cycle01/account.json` | `d21296d960f2d1b8dd853299caba7bdcb816cc8612e02c11eca4ca35c16e9213` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-07/artifacts/daily/mini_prose/cycle01/carry.json` | `92bb3d68e3e8222a659321171608d2e480cd236cd078ace32da9ebeb9ca5e19a` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-07/artifacts/daily/mini_prose/cycle01/objection.json` | `cc83ca89e521eae8552f71f2519d9cd965f31ad3c6284b84790c374e3d3d6de5` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-07/artifacts/daily/mini_prose/cycle01/response.json` | `4bbdddeb83fab3257237d44bb2877df3efb21dec6efbc24b0e2fd825759e3611` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-07/artifacts/daily/mini_prose/cycle01/rival.json` | `ee88630a8354f99c95c5270bd499182db0bc72d34453f0ae565f5ca136ac4c41` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-07/plan.json` | `1e34079c4af43132440d131e5d7a480dabc4cc15fb501cd4c38eeb6d7f97fb3e` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-08/arms.json` | `5f7cab0797a758e7e2de86e113d404f33b7a0e514482a7e8334398f3fec1e3b6` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-08/artifacts/daily/bare/cycle01/answer.json` | `2b9d51b870073f2fd1395027af01eb466207db016ac475e55ccdbcb73df50a32` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-08/artifacts/daily/mini_fcl/cycle01/account.json` | `1c9c81fec4eaecb74a13684d92293a1a8b7fb1c545195e525982045d920d2a75` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-08/artifacts/daily/mini_fcl/cycle01/objection.json` | `b74c3351c02ee4f98590cce6cd984be6d87d88e370dde7d778921a6fe2b87907` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-08/artifacts/daily/mini_fcl/cycle01/response.json` | `2324e79a0a3739e2d57691df66124b9f64444b0c27192b4f15a6c4d7647e3770` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-08/artifacts/daily/mini_fcl/cycle01/rival.json` | `313c6e0876cb4be25b9b0c8b76fcabfc825d0c3ee56b9264d4bda6acac6f58ad` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-08/artifacts/daily/mini_prose/cycle01/account.json` | `e91563ae39a2679e03342edbb5d6d13cc8da753cbcc3a17e3a93cfdd8ef0b46d` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-08/artifacts/daily/mini_prose/cycle01/carry.json` | `a92dec0e7cf88e32694d11395eb2669550f999875cae0d3d0bfccc6ecc7820d8` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-08/artifacts/daily/mini_prose/cycle01/objection.json` | `f4918bfbc72a19806a8fee7b4b8389a6d8e27b8db0c1f438848b2efa702ee306` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-08/artifacts/daily/mini_prose/cycle01/response.json` | `8d72427bb0cc42f61db62dfd6e263c6ab73db6c95525a589b052cf6095a72c49` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-08/artifacts/daily/mini_prose/cycle01/rival.json` | `b7fd76b43708ffbf5419a1db7d65c4e302d5ff37505157655cff10134252bcd7` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F001-fork5-multifamily/occurrence-08/plan.json` | `028c551106cc37c6f568fe559c79e784abe7c849f5372447291e22216e61a5f2` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F002-fork5-raised-clock/occurrence-01/arms.json` | `2a181f80eae29f0716be1fdcae1f67c38df38f096b6cbd7c7a344acbdf013b3b` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F002-fork5-raised-clock/occurrence-01/artifacts/daily/mini_fcl/cycle01/account.json` | `1ea4937b3d84e5aa06286e388d54b19d0e9db4e517993ff71b94b2c98c42ee5e` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F002-fork5-raised-clock/occurrence-01/artifacts/daily/mini_fcl/cycle01/objection.json` | `f1a838bfb9f6d172d5c4e3d37645f6c31b757525df47ad198ef0ddc74e449adb` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F002-fork5-raised-clock/occurrence-01/artifacts/daily/mini_fcl/cycle01/rival.json` | `65d7e4485db366af63e30d37aca2b2b8ef8a83e9b6970625bf9ba141de4ee8d2` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F002-fork5-raised-clock/occurrence-01/plan.json` | `bed7e150c5b116fcb60feaf1e9893f39d23c957af815e86c7c3400984f74e995` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F002-fork5-raised-clock/occurrence-02/arms.json` | `117d9584d9c559a5be9e7103ffdcd4864740f89a65aca9ee804b5384fb989cef` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F002-fork5-raised-clock/occurrence-02/artifacts/daily/mini_fcl/cycle01/account.json` | `968aa1c41706a929e97b35590df51f4f6f9b8228b33e3accf9ee4b6e582a2e51` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F002-fork5-raised-clock/occurrence-02/artifacts/daily/mini_fcl/cycle01/carry.json` | `aff3f6ca406a47739ae38526ef96ad601840e2ff6a3af7d5c5a7ae3b7e5b28c1` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F002-fork5-raised-clock/occurrence-02/artifacts/daily/mini_fcl/cycle01/objection.json` | `5d5b6e79dee79b52281c4d166d415e64e4dfef0c28f2956ef60b42518f7d59e2` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F002-fork5-raised-clock/occurrence-02/artifacts/daily/mini_fcl/cycle01/response.json` | `ad579ff00b132485b97455fa171c86b35f1158712bae6ef9fa41bb4b594d42e0` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F002-fork5-raised-clock/occurrence-02/artifacts/daily/mini_fcl/cycle01/rival.json` | `f18b99266bacec85a48c89bee4496f971be0265a7115361cb9ffc69917ab1a8b` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `F002-fork5-raised-clock/occurrence-02/plan.json` | `a4420dfbaff1ea9f5a3971be1f2b2ac9396e7edca7fde70daec9a49a39c7ef54` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `H005-open-prose-commitments/occurrence-01/artifacts/daily/bare/cycle01/answer.json` | `e28f6bd07d8acab50b870d613dcca840c8a1ef96f4c8ac99dac61baa4ded13c7` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `H005-open-prose-commitments/occurrence-01/artifacts/daily/matched/cycle01/account.json` | `4a53987178e4fcaf1ea3f3f61602c5cc50845d1bbaa657cf58827e65decad544` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `H005-open-prose-commitments/occurrence-01/artifacts/daily/matched/cycle01/carry.json` | `19078bf2ed169e74e18e9a682795f3fb5f8c63bf3bb1d53297a26fefa3970526` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `H005-open-prose-commitments/occurrence-01/artifacts/daily/matched/cycle01/objection.json` | `0bbcb5ee57a41ef655f687d3b0f8d9f8ffa399c893d48dae0995c72eb0e5bf8f` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `H005-open-prose-commitments/occurrence-01/artifacts/daily/matched/cycle01/response.json` | `dcd92f6694e2e0f216e24acd013515dcb4d30418a7cc371ae70a7a5e11b29684` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `H005-open-prose-commitments/occurrence-01/artifacts/daily/matched/cycle01/rival.json` | `aebb15d63ba6eebdc354896f6f113643df3e64e2081b2c702d09023a61afa167` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_fcl/cycle01/account.json` | `b8de6a8d579c358cade3296a7e8260a03c6e80269cd0486aae43c134999732e6` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_fcl/cycle01/carry.json` | `cfd3844e4207455171e31093b1f0c57ca0ca11ce1e456d0639b34d62a3401e79` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_fcl/cycle01/objection.json` | `810913b5c31f94a4d697da0e90e74205ac6b7abc7b217d44188852f2562110db` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_fcl/cycle01/response.json` | `a1d4f48d5246608ade51b63604beafc82de9770465d2a7fd7c2340ee8a4e55d3` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_fcl/cycle01/rival.json` | `b0b15d8d44c7dcd706879a9ced41e3f26a592ec5a25c2a961e01e32ea748e8cd` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_prose/cycle01/account.json` | `11bdb5753d4fe7e0bcf2b357cf37afe751e38157e9f1d676f9e32ce63e3f1005` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_prose/cycle01/carry.json` | `4a48f31e01d69c604fc516445534d36e8063802f5c6a148f93cdc34e5d5a5932` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_prose/cycle01/objection.json` | `7a331fe944fe20018b3087531e131ddcf3f0dd9eee3255e8a239036b0280ad06` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_prose/cycle01/response.json` | `442f65eaa131703c11cc0cbb9f9e55bf69c2a7d0dead6af41757749b17ae2df7` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_prose/cycle01/rival.json` | `e60b3d93f1bf628f637c05a03de32f0cc72441f3ef93a820747325cef0a6df52` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `H005-open-prose-commitments/occurrence-01/artifacts/daily/native/cycle01/answer.json` | `2a1c9b736de2300dbd6caab605d7bd07b7fbfbf5cd172d88ac5725b8bc5ba95e` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |
| `H005-open-prose-commitments/occurrence-01/plan.json` | `99cda29f3c6788d564448f7587c7448a6542d30a9bd5e48dc219925e2cc464c3` | MISSING -- referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox | neither base |

## `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-01/use-table/USE_TABLE.md`

- format detected: markdown table rows `| path | sha256 |`
- counts: {"MISSING": 32}
- Completeness claim: '## Nodes whose commitment surface was not read  *None in this scope.*  ## Residue: refs that resolve to nothing  | referring coordinate | record | field | ref | code | reason | |---|---|---|---|---|---| | `daily/mini_fcl'. Entry bases are the original study occurrence trees (experiments/diagnostics/...), not this analyses directory; the occurrence file name is derived only from the table's own custody header (H005 occurrence-0N). A row therefore can only be re-verified when the same bytes happen to exist under manifest-relative or sandbox-root resolution.

| path | recorded sha256 | verdict | resolution |
|---|---|---|---|
| `artifacts/daily/mini_fcl/cycle01/account.json` | `1ea4937b3d84e5aa06286e388d54b19d0e9db4e517993ff71b94b2c98c42ee5e` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `artifacts/daily/mini_fcl/cycle01/objection.json` | `f1a838bfb9f6d172d5c4e3d37645f6c31b757525df47ad198ef0ddc74e449adb` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `artifacts/daily/mini_fcl/cycle01/rival.json` | `65d7e4485db366af63e30d37aca2b2b8ef8a83e9b6970625bf9ba141de4ee8d2` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `attempts/daily/mini_fcl/cycle01/account.json` | `59878fd0d40b8e4de8c7121327fd3bc0000a32278cf597dda3fe18d0a8933583` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `attempts/daily/mini_fcl/cycle01/objection.json` | `42035b20082ef0a5fd2eee4abb6b880f5e77e80b4b12a4f82f0ceb97fab180cf` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `attempts/daily/mini_fcl/cycle01/rival.json` | `0b21efa0376c2c85d127ff39c9e4df169e31096b7ec33f23715defc04a11019d` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `manifests/fork5.json` | `8f2d928b2f70298906b17d62e73b41804efa754d845f018d9eb312af7dcb536a` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `manifests/return6.json` | `bad1f6dc4ddda462f1b3acaa56a9e552eeb98255509cb4bfa3353c2305abb3b5` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `manifests/weave7.json` | `0b8a5f337f754b23fd51721ff287e25347af99648a7d2b00ad73b7baa571c2cb` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `material.json` | `aadea004b4722fb1b4878bc9c46e7ba8ef5883ff6bcbff4aac10020b6b017679` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `plan.json` | `bed7e150c5b116fcb60feaf1e9893f39d23c957af815e86c7c3400984f74e995` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `provider/daily/mini_fcl/cycle01/account/call-0001.request.json` | `53e36d1754d47ed757cd3b0b5c62514d0a7429170bf610652ebf6a814c3606a5` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `provider/daily/mini_fcl/cycle01/account/call-0001.response.json` | `e6ef29e0c626042c67c0efed20b2cb9c3c9ac9183947cc249c70a01ea0e6358e` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `provider/daily/mini_fcl/cycle01/objection/call-0001.request.json` | `2eb57c31bcc6ee0cc8b7f32664565ace50c13a780c66b1e4c8a88b73dbc1347d` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `provider/daily/mini_fcl/cycle01/objection/call-0001.response.json` | `849d81d00fa5af107c0a6f2b16e3d4d95b829f4bbdd8d79895d2a56e3621deb5` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `provider/daily/mini_fcl/cycle01/rival/call-0001.request.json` | `f0ea42b66942f7403f7f6f016bf6eafbfb4dc6a2b0fc97fca9651f1a19b16547` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `provider/daily/mini_fcl/cycle01/rival/call-0001.response.json` | `bda1fe53eb093ee0c10422adf35dc433c004cbebbee8ce43ab1ea2341e86b09f` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `requests/daily/mini_fcl/cycle01/account.json` | `4d9836af307533b79d05ab6654ad6578035463b8db43fb01cc71056f715f9e1f` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `requests/daily/mini_fcl/cycle01/objection.json` | `272e9529233397821fbc8d6c22f4442f214191b3875bdf6fac56bbfa66f3cbd7` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `requests/daily/mini_fcl/cycle01/rival.json` | `5400e562f4f1adfa139210db81238fa5b4b31a4463dd5b34c8cb23e3883dc143` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `responses/daily/mini_fcl/cycle01/account.json` | `3c2b25ba89c9faf64c94b1a8e7697981d4bd017fd32fa71fdd60bc14b63b5b0e` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `responses/daily/mini_fcl/cycle01/account.txt` | `11d6110bd3b641f875d82290147dbd518680bd2f9c35cd540500f5050167216b` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `responses/daily/mini_fcl/cycle01/objection.json` | `a97b586f9803277b7c9a1a1c5765b6dc7866371458273d5c37f8875c4f7c665f` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `responses/daily/mini_fcl/cycle01/objection.txt` | `d98c6b2485cb1394f8846689bc4523039a8bb8682c58ee65cebb7ed0dd6fe1d6` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `responses/daily/mini_fcl/cycle01/rival.json` | `d651dde8336d2e9a82dac98b91ee2fe38c85fc7d1be3fb0714e30341dc3fb34c` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `responses/daily/mini_fcl/cycle01/rival.txt` | `438c4fecfe2c2449464560527e8785d4fc120afe056590883a901fa7cda56001` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `traces/daily/mini_fcl/cycle01/account.json` | `f4790106152ef33f8f02cc8f182089bd4e99beb4f553144a79e51e2ec4f92f53` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `traces/daily/mini_fcl/cycle01/objection.json` | `2c8ca9a4f6da717a4b3f11fae071df6c9622ed076eaee3a55236491359b521e7` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `traces/daily/mini_fcl/cycle01/rival.json` | `f7cf8b5680bed9a2444f2225af990246bae112b305ffbece136f52653828d92c` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `waves/wave0001.json` | `811db21379fb35385cb377860b62f385de0cac9f425fdd188cc5a1b21883cadd` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `waves/wave0002.json` | `b9eef0e7974e217a7efb65ad62e85d6773589d059bdde011399939f097eee65a` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `waves/wave0003.json` | `ddb44215ccff56d7c2616819a764e0ae90ffb9189d86818db6f02e717b2ab462` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |

## `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/use-table/USE_TABLE.md`

- format detected: markdown table rows `| path | sha256 |`
- counts: {"MISSING": 49}
- Completeness claim: '## Nodes whose commitment surface was not read  *None in this scope.*  ## Residue: refs that resolve to nothing  | referring coordinate | record | field | ref | code | reason | |---|---|---|---|---|---| | `daily/mini_fcl'. Entry bases are the original study occurrence trees (experiments/diagnostics/...), not this analyses directory; the occurrence file name is derived only from the table's own custody header (H005 occurrence-0N). A row therefore can only be re-verified when the same bytes happen to exist under manifest-relative or sandbox-root resolution.

| path | recorded sha256 | verdict | resolution |
|---|---|---|---|
| `artifacts/daily/mini_fcl/cycle01/account.json` | `968aa1c41706a929e97b35590df51f4f6f9b8228b33e3accf9ee4b6e582a2e51` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `artifacts/daily/mini_fcl/cycle01/carry.json` | `aff3f6ca406a47739ae38526ef96ad601840e2ff6a3af7d5c5a7ae3b7e5b28c1` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `artifacts/daily/mini_fcl/cycle01/objection.json` | `5d5b6e79dee79b52281c4d166d415e64e4dfef0c28f2956ef60b42518f7d59e2` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `artifacts/daily/mini_fcl/cycle01/response.json` | `ad579ff00b132485b97455fa171c86b35f1158712bae6ef9fa41bb4b594d42e0` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `artifacts/daily/mini_fcl/cycle01/rival.json` | `f18b99266bacec85a48c89bee4496f971be0265a7115361cb9ffc69917ab1a8b` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `attempts/daily/mini_fcl/cycle01/account.json` | `5624baaf47e6e69b73243c907d8221522bb23007964712434bfe5b9f564c7a76` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `attempts/daily/mini_fcl/cycle01/carry.json` | `c4b29373340531802d8b564df6e054852831f58171aa3036f67f3051306b4cd3` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `attempts/daily/mini_fcl/cycle01/objection.json` | `31f1c7b6af5ae047407259db24909074b20795d6b6f11543cc68ab757c6b08a5` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `attempts/daily/mini_fcl/cycle01/response.json` | `7820843b8e040b888e640e11f4c376a04a392b19c6f4c702bc15f9d436c0378b` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `attempts/daily/mini_fcl/cycle01/rival.json` | `623b715be2b2d422b66616279a3c3e910e57e86dfe48a3d8066e89218867620b` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `manifests/fork5.json` | `8f2d928b2f70298906b17d62e73b41804efa754d845f018d9eb312af7dcb536a` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `manifests/return6.json` | `bad1f6dc4ddda462f1b3acaa56a9e552eeb98255509cb4bfa3353c2305abb3b5` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `manifests/weave7.json` | `0b8a5f337f754b23fd51721ff287e25347af99648a7d2b00ad73b7baa571c2cb` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `material.json` | `aadea004b4722fb1b4878bc9c46e7ba8ef5883ff6bcbff4aac10020b6b017679` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `plan.json` | `a4420dfbaff1ea9f5a3971be1f2b2ac9396e7edca7fde70daec9a49a39c7ef54` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `provider/daily/mini_fcl/cycle01/account/call-0001.request.json` | `76ef5edd5d1f3f36e537a085cd977072e2fd91247e2d7d81e4900feb694c61c4` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `provider/daily/mini_fcl/cycle01/account/call-0001.response.json` | `d5c5075b59fd1c599d26e237a8caed94afeb3c5afcb6261622f5a260f274b76a` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `provider/daily/mini_fcl/cycle01/carry/call-0001.request.json` | `7ddc4d7c6e00c50d702326bb093722bb1446f3a0e217d56230d4cfb442b8015a` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `provider/daily/mini_fcl/cycle01/carry/call-0001.response.json` | `8a12bb5447f1b6fea89fb325f359bc841358b615f735c397b81dcbd969973548` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `provider/daily/mini_fcl/cycle01/objection/call-0001.request.json` | `fc834104d86d012cf4aafe30f86b7f2d95b04ec1a7d816dd8b8b14ea12de5312` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `provider/daily/mini_fcl/cycle01/objection/call-0001.response.json` | `a80309b9f784f339d8d7cd1ad42aada658787a1fe5f7d27e35080d2450d81975` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `provider/daily/mini_fcl/cycle01/response/call-0001.request.json` | `30bbd1203dd9112ba7e3f660fe5d23115e46fe113c11eae6bd47a8f22e90403b` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `provider/daily/mini_fcl/cycle01/response/call-0001.response.json` | `44504da99e7ba7b7a5fbaff4aed96dbb23d531893b91779b174c9721776c3cd4` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `provider/daily/mini_fcl/cycle01/rival/call-0001.request.json` | `63b6e7502133cd1b40d5b7e959b9ac5e7de873966bbd776153d6c2938a00b89b` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `provider/daily/mini_fcl/cycle01/rival/call-0001.response.json` | `cb34667256f179b2df128f5815d7d5afa8c388700fae18d8fd3c6ed72e598b3f` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `requests/daily/mini_fcl/cycle01/account.json` | `fb3f0aaa79e3f036b9b992ec4644dd637344502057837ea12060ee0e743fe720` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `requests/daily/mini_fcl/cycle01/carry.json` | `0e2961c5eb70670da4def8a4e6b3d543c69e476d6261b3ff496219ed8a8a8764` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `requests/daily/mini_fcl/cycle01/objection.json` | `3268a066b48b4e7a35b84a4df1dffd0da86ded54d4a8593e1bbdfeeb3ac16dbe` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `requests/daily/mini_fcl/cycle01/response.json` | `e5b47c0ead2e3552ba17646ef341eb3dfbdaa42e1def2a7dd5da2c443bfbaf0c` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `requests/daily/mini_fcl/cycle01/rival.json` | `bf9d85fe9a1e90e218b146e1e1a8c001ad8ae9a9adea8445eb07ff38a346fb18` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `responses/daily/mini_fcl/cycle01/account.json` | `35242bad7cf6e82c7a148cddda1256fce226ab06cddc8b03c1e0bdb39c080c26` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `responses/daily/mini_fcl/cycle01/account.txt` | `e7bd8672abee3460471194a1a3065a5b87ca655b787508693a367db1d73f9dd1` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `responses/daily/mini_fcl/cycle01/carry.json` | `6031aae11595f7527a552d46a32677bb8a9cdcd8eb0c8366a893a6647297c527` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `responses/daily/mini_fcl/cycle01/carry.txt` | `a4662a89cd02b3a767bf708e7f8feb72b66637e7753b948ac1cae36663f3aea1` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `responses/daily/mini_fcl/cycle01/objection.json` | `c4b0c2934232c0f873fe50b2c1f0e8e46d071fe7661153bd7967a8a5ccd45352` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `responses/daily/mini_fcl/cycle01/objection.txt` | `105c9afe90b1e09192262a63f8480dafb794372e73d3484fdaf6eb85ba929fcf` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `responses/daily/mini_fcl/cycle01/response.json` | `3515f29d751c20021171bbfc7d6d6c4179e32b94385eba3b2585eccee80c3942` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `responses/daily/mini_fcl/cycle01/response.txt` | `97b610e08a1f41a7b3e8a7c43940c947ca84828eaa67b42f34e420e407016c27` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `responses/daily/mini_fcl/cycle01/rival.json` | `f564fb728cb5016aa0b85a25df479ff99c81ecbec39700f96a91a29df7a4a3d7` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `responses/daily/mini_fcl/cycle01/rival.txt` | `7b65fccfa2e3bcc58b5ea73475eb3b8c4d79eff2a244095929ed014738eeb1c0` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `traces/daily/mini_fcl/cycle01/account.json` | `f4790106152ef33f8f02cc8f182089bd4e99beb4f553144a79e51e2ec4f92f53` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `traces/daily/mini_fcl/cycle01/carry.json` | `569787c26f109beefd3434ade9cd4800d407751dc4089d9f95f0a07512c2ca3f` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `traces/daily/mini_fcl/cycle01/objection.json` | `333713cdc14311614bac2b4cc6f86ca92d7b7a133c770f224f96cb8e3999658b` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `traces/daily/mini_fcl/cycle01/response.json` | `afb13ce83e1e885a0d1e840344f6a6f8bdcf3d253ba489f2bca30fe18bcd3db7` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `traces/daily/mini_fcl/cycle01/rival.json` | `3912ba306f34e65a76b3e209e5d7b4dc9b522bf5260e8f6a2561e8f43f843f71` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `waves/wave0001.json` | `e048b42bf69236bf32fd8c31f3a1b41c0d511e92f5ead634fab667d4d1a03ab5` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `waves/wave0002.json` | `c80c5c9f8111df0502e8bce18d898462cc47a0ab9cd68dacd2c35ed3539b2d86` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `waves/wave0003.json` | `205b23346724b057cb12d71ffc4b516222258d0084fa7548455d040062ca2f87` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `waves/wave0004.json` | `193faa973d6342fe5a523b1ccd510a0312d893a53fb5e3b1b8264181182cf4fb` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |

## `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-03/use-table/USE_TABLE.md`

- format detected: markdown table rows `| path | sha256 |`
- counts: {"MISSING": 23}
- Completeness claim: '## Nodes whose commitment surface was not read  *None in this scope.*  ## Residue: refs that resolve to nothing  *No unresolved ref in this scope.*  ## Files read  Every byte this instrument read, with its sha256.'. Entry bases are the original study occurrence trees (experiments/diagnostics/...), not this analyses directory; the occurrence file name is derived only from the table's own custody header (H005 occurrence-0N). A row therefore can only be re-verified when the same bytes happen to exist under manifest-relative or sandbox-root resolution.

| path | recorded sha256 | verdict | resolution |
|---|---|---|---|
| `artifacts/daily/mini_fcl/cycle01/account.json` | `c2fa20c2207f5101769613ac3f509a77fc29cac22ef1f6a65fd5f02e623e7834` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `artifacts/daily/mini_fcl/cycle01/rival.json` | `402e859a9e05056122a7342538b25a54fd17ab513cf1438ec35be272cd84babf` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `attempts/daily/mini_fcl/cycle01/account.json` | `802119c5790d2c264fd768450f4d4c80ee23f1ad230ab7c55d27a61adbfd48ab` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `attempts/daily/mini_fcl/cycle01/rival.json` | `3a0aa3bcf2f5e3babecd22e7a26b346ee1cdddbe2d29b3fdc2f69759b652a843` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `manifests/fork5.json` | `8f2d928b2f70298906b17d62e73b41804efa754d845f018d9eb312af7dcb536a` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `manifests/return6.json` | `bad1f6dc4ddda462f1b3acaa56a9e552eeb98255509cb4bfa3353c2305abb3b5` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `manifests/weave7.json` | `0b8a5f337f754b23fd51721ff287e25347af99648a7d2b00ad73b7baa571c2cb` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `material.json` | `aadea004b4722fb1b4878bc9c46e7ba8ef5883ff6bcbff4aac10020b6b017679` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `plan.json` | `bed7e150c5b116fcb60feaf1e9893f39d23c957af815e86c7c3400984f74e995` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `provider/daily/mini_fcl/cycle01/account/call-0001.request.json` | `bb60087d00a790b8bf7f07e65a3cd9f8a83efd7e895027e95913016052222112` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `provider/daily/mini_fcl/cycle01/account/call-0001.response.json` | `4f5f54030b593ee38c89a998ba068eff5c1990c865706eb6b35ed94d79a708ff` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `provider/daily/mini_fcl/cycle01/rival/call-0001.request.json` | `de0af1cdf278c9cbb06b63f45eee333062adf86e2761481d14f57a8f869b8715` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `provider/daily/mini_fcl/cycle01/rival/call-0001.response.json` | `ff5653e789ad7b50719ba15aa7003b31a3674b574f1bea3e9a2df4fb966e2070` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `requests/daily/mini_fcl/cycle01/account.json` | `4d9836af307533b79d05ab6654ad6578035463b8db43fb01cc71056f715f9e1f` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `requests/daily/mini_fcl/cycle01/rival.json` | `a4f41495f4f2a498505791af5584355c0248d687d36480255697057b7375184c` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `responses/daily/mini_fcl/cycle01/account.json` | `79a4f545e1fad4e5556dd8de8fe80b4d1826b2256feab527546dbda95f8acee3` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `responses/daily/mini_fcl/cycle01/account.txt` | `e39c114c2e7a25b1d320d70d528f72ca2c1de39dea7fc147d4deac9744cdfcb0` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `responses/daily/mini_fcl/cycle01/rival.json` | `a615ffd9ff81a0f33de2e7e1e2405315fdb86f2ed15fb515bae19f7bdc71844b` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `responses/daily/mini_fcl/cycle01/rival.txt` | `82719e25c2b7c66ef34c28a6b49e4fef673f604dbf6991192e15a0aa20c740f0` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `traces/daily/mini_fcl/cycle01/account.json` | `f4790106152ef33f8f02cc8f182089bd4e99beb4f553144a79e51e2ec4f92f53` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `traces/daily/mini_fcl/cycle01/rival.json` | `7c25d8128dda6536868fa3193ea0554fb8c9a9ff018f8f693364403b78454f63` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `waves/wave0001.json` | `811db21379fb35385cb377860b62f385de0cac9f425fdd188cc5a1b21883cadd` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |
| `waves/wave0002.json` | `cfb4dd06c3035e8ce6cc30514265a62072f891794067df9aa39bac86135fd886` | MISSING -- referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory | neither base |

## `experiments/diagnostics/C001-contrast-triple/PLAN.md`

- format detected: markdown table rows `| path | sha256 |`
- counts: {"MATCH": 2, "MISSING": 1}
- Rows pin material/driver by repo-root path; the driver tools/contrast_triple_study.py was not copied into this sandbox.

| path | recorded sha256 | verdict | resolution |
|---|---|---|---|
| `src/minireason/provider_openai_compat.py` | `cdc4b5711263eae2eebf9eadda3a52ad7b9c1f2320a780adc955bcb3cdaee5db` | MATCH | sandbox_root (src/minireason/provider_openai_compat.py) |
| `src/minireason/data/endpoints.json` | `03eff16b8f575c113871a1266439874b2622a75d200ecb84a1b79464aa98aee7` | MATCH | sandbox_root (src/minireason/data/endpoints.json) |
| `plan_id` | `328b9452c66fed52203015c540652d3b8ad3107d44dece56b55ebe721da341c8` | MISSING -- pinned bytes not copied into this sandbox | neither base |

## `src/creib/forge/mini/manifest.py`

- format detected: filename match only (not a digest list)
- counts: {"UNPARSED": 1}

| path | recorded sha256 | verdict | resolution |
|---|---|---|---|
| `src/creib/forge/mini/manifest.py` | - | UNPARSED: filename matches the manifest rule but the content is not a path->digest list (it is source code / a template-schema JSO | - |

## plan.json identity statements (step 4)

| plan | top-level keys | plan_id | derivation statement in a sibling file |
|---|---|---|---|
| `experiments/diagnostics/C001-contrast-triple/occurrence-01/plan.json` | `arms`, `briefs`, `cases`, `ceilings`, `claim_ceiling`, `coordinates`, `determinism`, `endpoints`, `envelope_unwrap`, `helper_sha256`, `material_sha256`, `node`, `partial_delivery_rule`, `plan_id`, `planned_calls`, `question`, `reading_rule`, `record_layout`, `replicates`, `schema`, `seed_policy`, `seeds`, `source_pins`, `study`, `transport_pins` | `328b9452c66fed52203015c540652d3b8ad3107d44dece56b55ebe721da341c8` | experiments/diagnostics/C001-contrast-triple/PLAN.md: “plan_id` = digest of the frozen plan body; minted by `prepare`, written to `plan.json`. For the published material and driver: `328b9452c66fed52203015c540652d3b8ad3107d44dece56b55ebe721da341c8`. It supersedes `34f5101702” |
| `experiments/diagnostics/C001-contrast-triple/occurrence-02/plan.json` | `arms`, `briefs`, `cases`, `ceilings`, `claim_ceiling`, `coordinates`, `determinism`, `dispatch_scope`, `endpoints`, `envelope_unwrap`, `helper_sha256`, `material_sha256`, `node`, `partial_delivery_rule`, `plan_id`, `planned_calls`, `question`, `reading_rule`, `record_layout`, `replicates`, `schema`, `seed_policy`, `seeds`, `source_pins`, `study`, `transport_pins` | `1d9f47acdc692146792e354afdd9c6944036cb7d55bd83cc32c905e7c4ffeb83` | experiments/diagnostics/C001-contrast-triple/PLAN.md: “plan_id` = digest of the frozen plan body; minted by `prepare`, written to `plan.json`. For the published material and driver: `328b9452c66fed52203015c540652d3b8ad3107d44dece56b55ebe721da341c8`. It supersedes `34f5101702” |
| `experiments/diagnostics/F002-fork5-raised-clock/occurrence-01/plan.json` | `arms`, `arms_sha256`, `automatic_retries`, `ceilings`, `cycle_definition`, `envelope_repairs_declared`, `formal_syntax_validation`, `helper_sha256`, `key_environment_names`, `manifests`, `material_sha256`, `max_calls`, `max_calls_envelope`, `max_concurrent_requests`, `max_concurrent_requests_per_key_env`, `max_concurrent_requests_total`, `partial_public_continuation`, `plan_id`, `provider_mode`, `provider_pins`, `providers`, `runner_sha256`, `runtime_pins`, `schema`, `scope`, `settings`, `source_pins`, `study_id` | `9aa92a837569bd56a86b172eb56dd80dbc69c519a86286d3387b020c2709a0d5` | experiments/diagnostics/F002-fork5-raised-clock/PLAN.md: “plan_id` is a digest over the material, the” |
| `experiments/diagnostics/F002-fork5-raised-clock/occurrence-02/plan.json` | `arms`, `arms_sha256`, `automatic_retries`, `ceilings`, `cycle_definition`, `envelope_repairs_declared`, `formal_syntax_validation`, `helper_sha256`, `key_environment_names`, `manifests`, `material_sha256`, `max_calls`, `max_calls_envelope`, `max_concurrent_requests`, `max_concurrent_requests_per_key_env`, `max_concurrent_requests_total`, `partial_public_continuation`, `plan_id`, `provider_mode`, `provider_pins`, `providers`, `runner_sha256`, `runtime_pins`, `schema`, `scope`, `settings`, `source_pins`, `study_id` | `a59debaf6382ce7c01c4c07d14894890736e2a960b66d4323f9eb84ac72b1163` | experiments/diagnostics/F002-fork5-raised-clock/PLAN.md: “plan_id` is a digest over the material, the” |
| `experiments/diagnostics/F002-fork5-raised-clock/occurrence-03/plan.json` | `arms`, `arms_sha256`, `automatic_retries`, `ceilings`, `cycle_definition`, `envelope_repairs_declared`, `formal_syntax_validation`, `helper_sha256`, `key_environment_names`, `manifests`, `material_sha256`, `max_calls`, `max_calls_envelope`, `max_concurrent_requests`, `max_concurrent_requests_per_key_env`, `max_concurrent_requests_total`, `partial_public_continuation`, `plan_id`, `provider_mode`, `provider_pins`, `providers`, `runner_sha256`, `runtime_pins`, `schema`, `scope`, `settings`, `source_pins`, `study_id` | `9aa92a837569bd56a86b172eb56dd80dbc69c519a86286d3387b020c2709a0d5` | experiments/diagnostics/F002-fork5-raised-clock/PLAN.md: “plan_id` is a digest over the material, the” |

## Cross-manifest claims re-computed

- from `experiments/analyses/F002-fork5-raised-clock-2026-09-14/README.md`: "material.json and all three manifests are byte-identical to occurrence-01's" (occurrence-02 and -03) -- **CONFIRMED** (sha256 comparison of the four files under all three diagnostic occurrences): material.json -> byte-identical across occurrences; manifests/fork5.json -> byte-identical across occurrences; manifests/return6.json -> byte-identical across occurrences; manifests/weave7.json -> byte-identical across occurrences

## Files present on disk that no manifest references (informational)

### `experiments/analyses/F002-fork5-raised-clock-2026-09-14` (139 files)

- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/README.md`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-01/audit.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-01/import/REPORT.md`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-01/import/blobs/05/05f9b4faf00cd8034ec3859437353a511eff571e0b89f767834acb2b4a171b60`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-01/import/blobs/3b/3b1267166dceab12e86d4b2fe166c85e8a49e61e8ede85e225c3ffb15cd2dbb0`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-01/import/blobs/40/40bdb1a79ec7316267f0b4ab52057f607744cd205027b3e91941b2280490aaea`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-01/import/blobs/5e/5e52c5b03a997cbd179c9e57f816487e662b9cf185496c4261af57adad7a4349`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-01/import/blobs/8b/8b9bfb166833667945faaaaf8aa57b490745070e55fa05d399674c55cb2db6b4`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-01/import/blobs/9d/9d7f715d67f159bbed63baec213260a3332b3da6e685f8e51628c94c74d89474`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-01/import/log.jsonl`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-01/import/objects/artifact/0fc2ae627c9d0152bf58b3c954beae9496bbfec90df21afa6c7340679a48643b.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-01/import/objects/artifact/2c80547dd946a53612725efa97dc5c29ebe8a351ec773826e2237e42cfeeb3e7.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-01/import/objects/artifact/3567d840c1dcd1b5d85a15a778df2cf12522e6cb757782bd729279cc84e91b23.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-01/import/objects/artifact/42f1fb5b40d9037d40f24700d8df953299dde2a94232da877fd31b2b959c6aa7.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-01/import/objects/artifact/51580f0ba7d836346254a3c93053340f90baee2990dc404fa9f6eba5162229bf.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-01/import/objects/artifact/7e1cf72c27117f7693e36aec0a127d6f8a02843d7d4fdad6352750e6fd96fd98.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-01/import/objects/commitment/0dd7d6e1a7f92eec90aa912b9a821916c2c6f5140c0fb82b00db7ca76c1bacce.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-01/import/objects/commitment/51e0112a0aad491d1244ec1a0fae48bac07ccce621cfa45a7a1aafa368af622e.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-01/import/objects/commitment/5d5c4d6f315ba4532163fca63dbb55ca4889411dfca77a64c9b8a374e189acbf.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-01/import/objects/commitment/5f04ca95ec794ba9f0900225caacd693966e84edf9526b42e87d95c7ef2cb8a1.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-01/import/objects/commitment/8b897bcf8be2dcf32d1411504942714bacdbb962f25d4447e82bbf2f176c657c.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-01/import/objects/commitment/d17a194d8c3f57daf7c9d180af6bb3ca1ac50b36824daf8266af3a2fae656241.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-01/import/objects/commitment/fa21aa841c325bc5d363d22dc495d8fe53f9d623fa0d828d9362cf0b35f23b4a.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-01/import/objects/problem/0f7a68bfa1977f914fd595fbb2e2855a1a39cea9a0b96e304b94b5dced33d91b.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-01/import/objects/problem/22613abe1b812d91ebf9ce031a13016bda00080f017a7005545656a988385136.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-01/import/objects/problem/3dabd65300d032d76a40555cd6184cebe4c57bf38eb609fa15e33531a1507b41.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-01/import/objects/problem/4348e59995c9cf7496a84819db805ccb21cc90230f9d2857e6db166033de7401.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-01/import/objects/problem/52a2bd39a20423e3d2e89e2e067725deca37cf8f94eff6cb1a56640d8f7f04d6.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-01/import/objects/problem/657801d78fc4d99271efa685e20a8975114839c30e178016f14e3a2d2d3bdc8d.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-01/import/objects/problem/73c6266ecbb60ba7e607e17c0fda8abcbf651719a4240a5a7fd9e019b0055692.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-01/import/objects/problem/76eb2c83b42b0160088b200fa2731e2167e5ffd977a243735508fdea0d7c2ebe.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-01/import/objects/problem/7a8c974ac8b1f125b2357adf0a73b6a3e09a67fd14f499d66efe66bebde12903.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-01/import/objects/problem/837524777a02f29202c367b5911100c2ddb9a02993e91441f894887af11e1f29.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-01/import/objects/problem/adf455ebd210511967058e235d886faaaf69b9f193e707072dbe0764ca0b8bd1.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-01/import/objects/problem/af8f9a6d36a1cd9d509885e39cbc5a7cdea09cfa556651d73ed823997c4f4c8a.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-01/import/objects/problem/b56eaeae1f9ed4cc13c5fb31c2a0f3ee47198e73696c10ef682730bc189c43d6.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-01/import/objects/problem/b841f49019eb5335a4941d08e8549fade66c741ccf3e6def5dea2dd66e151a14.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-01/import/report.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-01/import/residue.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-01/import/side_table.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-01/use-table/USE_TABLE.md`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-01/use-table/use_table.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/audit.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/import/REPORT.md`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/import/blobs/4a/4a8afd18bd186db4526d3fd0c17e6670ca142b23b30377fda870113e09af0e1f`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/import/blobs/68/6808878e424014e8b9ac5114488ed292b97cfc7d1cdb617d791e3c4b2c39b787`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/import/blobs/6d/6d10a22a12dcdd48d0988c68d6e12d6cef7437201f8e1a62d5a01c542aaaf3f5`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/import/blobs/6f/6f51b2a0439a5b3e1d18dbf3d3a2b2c9afd72a94ca5e8e33e32bbbe20b74b2b5`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/import/blobs/86/86c2be1b34227ff6857e9b90f5af5ed0d833ee3a75bed7ad13a47bce942f8511`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/import/blobs/8b/8bcfd9b48a490408fc703397839d2d300f8c881a1ac0a98bcb3840c2b902785e`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/import/blobs/96/96a731eb112acd30b77f25f853f31f73e23bde6a758cc05dcf70f898410c58ef`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/import/blobs/9d/9d6ada829a2ed1da1885b50c4bb5e08efbaf57677ec303843e226e5335be8d7f`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/import/blobs/c2/c2be72fd0b56da9b993809fc2bcb8faaffaf4f8a97123811c1938858e5d3dc43`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/import/blobs/de/dedc07dc3691751d9f899628ec446833264440eed8a27b5618cdb25ebdf07ed2`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/import/log.jsonl`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/import/objects/artifact/0cc3bddc3617b4323b7431e1ac8d898a35ae316c6aa22d7772c037d2a95d5ab4.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/import/objects/artifact/235d787725e76becb97a6c692ed1c093de33964a0774416d29e3ad96fc0add9a.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/import/objects/artifact/4315428d221a776d235b1e2ade3bf594cc861ea14862b63eb2614d3a68cde217.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/import/objects/artifact/574ff588cd537c46867acefc1568de9caa503c8b653f7508a6abf27e2f8530e1.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/import/objects/artifact/7352a6112ced428dcd2b393b41a7fe10ddc768d64fa4bb80e2762a4aa8876974.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/import/objects/artifact/cab9e2763ecf32140d0f051f75514288143de3a67f588630db1c2fe02ca11561.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/import/objects/artifact/d1e027048d3a3236f3b65d8186aa1623d9b11a379327df938048367aae54177d.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/import/objects/artifact/df42ccd9cb7a59f80429a740469a6da1bd4bb2b997df12b24b5678327c5fb0de.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/import/objects/artifact/e56dd54c48056eab4cc494589dd04a4024d9cde47e0ba52f647af6c50ee95a4c.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/import/objects/artifact/f0fd317ba736cc2a92b68de06c111aea45d967d7b71ca0fb15e7b9a406cba7d9.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/import/objects/commitment/0dd7d6e1a7f92eec90aa912b9a821916c2c6f5140c0fb82b00db7ca76c1bacce.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/import/objects/commitment/6939937d436ad7c6d63e122507f08b952d0281c7895a22bb007c839f61c5d6d0.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/import/objects/commitment/74171127baa6e80fecdc53ff62c5428b3a422dff766d9668bcefe01c8c33569c.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/import/objects/commitment/89a9b2d81cb2918a1a6bb12cf4e1b0a160d9ed974f71c7bfecf2a62863f6cc8d.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/import/objects/commitment/a0103c0c8b527fdc729f87d27d866fd9f90ff9e5e72218a42bf5019481c4ecb9.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/import/objects/commitment/a11c65a777dc908ab426c2ab364fa444bf2f91293d0c282412dec1b66f0b2fda.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/import/objects/commitment/ae2062c1dfd900445cc32cd3b283a2350983718bcfd1f5845093e26c5fb78f6a.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/import/objects/commitment/d99e62486ad91357f0e10067e2a4a8401a0d13d012a5683a9a99af7e4652708d.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/import/objects/commitment/db8a2503fc56dc26859d886510e081093b6d9777a66c652623d43939521195c6.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/import/objects/commitment/ef37a921790819c0eeba9612a9f0eea2cbda515e3b306e9a663385eb714d9553.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/import/objects/problem/067fbf7445f7fbc73b75cd187298bf31f7f6fc2dedd1b4687313db11d81a41a0.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/import/objects/problem/0f7a68bfa1977f914fd595fbb2e2855a1a39cea9a0b96e304b94b5dced33d91b.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/import/objects/problem/1f2ad87735a4f22fcbb1698f93bad0da62c20f2ece7adcb76b8ab5a883e8dee1.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/import/objects/problem/1fc8288b609b29e96a47d2546d4815dd15371e234d44af915e0711c9042d0ad9.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/import/objects/problem/226f03ce72e467d61941d24c6b652338e51b78427e985995075e2c88a49be8a3.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/import/objects/problem/270b6305615b244d3b7fa497b94ca9e2358b69047fdd46e4455726a6526b9143.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/import/objects/problem/383bddee061fa837ee343decf87a117aefeed0414d7e78045b8a5163d5676f18.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/import/objects/problem/3dabd65300d032d76a40555cd6184cebe4c57bf38eb609fa15e33531a1507b41.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/import/objects/problem/592ebc48c9e6af28b1b0702522b66d4364f4de146b5a6870d429a6c97a5d61aa.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/import/objects/problem/5a8d7af8169cd4d74cd469cbe279f41a0eddd1a3c8555b7c2b664773656593de.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/import/objects/problem/617023e059d1ee81f22979c999da8d69566918710e32804124aadec912dc7bf7.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/import/objects/problem/682fd38339d1f79896013a54ec11f955770829169dc4d9692cfb8ffd23e2c48d.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/import/objects/problem/6ae20a12d35e9269a425d7c521b2ef9364d5b5849ca98b83fafebc4dc044b0c9.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/import/objects/problem/6f8923847fb83c2458033bef4ce0ed581f2debd3f37fc839fdf7a75f16fb10ed.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/import/objects/problem/710ac36f6bd3d47432e4ca4ca6909af081c6c1e33935271c52b6b9d8e74f2c69.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/import/objects/problem/71175b835f1be5455321035c1f357f01dfa0245a6b000dbe3b56eb1981f8967f.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/import/objects/problem/81e617b639d062ed161273c556a3639f6f37844ff18515ce5711e9d2538ac5b6.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/import/objects/problem/89eedbcd358a801048a7b1f291fe8ce89b45b48656973746d0c2c61eb9676c10.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/import/objects/problem/c02f00657a9084c300a517bf821a4fc43a20f9975792fce4577814397e0f02ba.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/import/objects/problem/cd7588609277e75a379e9322b65fede3eef4c41e09c8b4abe0258110a5e773fc.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/import/objects/problem/f6b64493db3283a949165a06219fa88fd06e904e5ddfa2adb29fe176911aea43.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/import/report.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/import/residue.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/import/side_table.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/use-table/USE_TABLE.md`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/use-table/use_table.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-03/audit.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-03/import/REPORT.md`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-03/import/blobs/1b/1b4072d0c42465cf0897021119978d18e78a13cefcb3d1b56da38e58a23090d5`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-03/import/blobs/37/373147558bd515ab709b11159b9c86e212e4acd6d5b4340e560b3781c4e18c68`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-03/import/blobs/73/73abff120e793c6a2c3a052aaac4f3b87871ce47605cd98a02b19a4bd76c0cd9`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-03/import/blobs/ee/ee61ca8db2e34171b6ab85b3df75a8a4828ba33d18778afe48fb0e246ba9e200`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-03/import/log.jsonl`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-03/import/objects/artifact/a667135eaeb605f671aa848d5f70bb944f7f9b372bafa880e4aea29abb151fff.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-03/import/objects/artifact/a82e4ad6d44a0db4f397ab06cf56a13e8d3ffa521571fc2b132e6fcfa7e584a7.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-03/import/objects/artifact/ef9de4c4a4c52934130f8d1e0c279153126ec4b6e9df4c3313ab916b2b16f015.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-03/import/objects/artifact/ff1f55a4db4e1de39b9d9138fe08172cb3f277c1016dbdbb95ceecd11be83355.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-03/import/objects/commitment/148b16cbe488e029df00f9c7e4b80e2fe1d2e901f0c3c16f3e57c1fe6695e750.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-03/import/objects/commitment/1f7a099ad8980fd6906fd1e2d2a75d827f6454ef1ea789ff7603302743d484f1.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-03/import/objects/commitment/4152ff9956f9440c993cb22932b965c5b95859026b6268123cd9bc7ef7572efa.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-03/import/objects/commitment/94bd73794c51df062ddf2234dcd7591cb5bb1aa96b92e69f214627f8b5b8a4a6.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-03/import/objects/commitment/a2754dd2f8eda143759796b5866d1f57655815948829df58d7574fc79b6deff6.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-03/import/objects/commitment/d4d603726c22b1555b7bdbf1391a4b049de933d22771305c8a7339e7b0ae6f78.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-03/import/objects/commitment/e0acc4a63c3c4830cc241a371b554f7a453055cdf2fb7fe3b32bc14176b4ea57.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-03/import/objects/commitment/f73cbc4e3f2cfdb0ad7cc3349ae6d1b48339b0ebab87f81f59b473e3245779e6.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-03/import/objects/problem/1f2ad87735a4f22fcbb1698f93bad0da62c20f2ece7adcb76b8ab5a883e8dee1.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-03/import/objects/problem/36d61b438858ababb50ab3ab40a336a4570d548b6d5c9cec747a91c689c0cc5b.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-03/import/objects/problem/3dabd65300d032d76a40555cd6184cebe4c57bf38eb609fa15e33531a1507b41.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-03/import/objects/problem/66049affe31083c90eb4152a45d4ef9c72225b65952539523d5a0151f97f4dec.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-03/import/objects/problem/6ae20a12d35e9269a425d7c521b2ef9364d5b5849ca98b83fafebc4dc044b0c9.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-03/import/objects/problem/70f18f41222736b4a70b5d539fe912e2083f5fcb207cf8e19f0435470ab82c67.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-03/import/objects/problem/73baf0f633f638319e91c7526b1b24fb4c6f828cbd5f26b1a5124d9b915c9f2a.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-03/import/objects/problem/8c3e5c7aa351c2183a43e1ecd49a5d15f6170ad2538489d3fb54865852988977.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-03/import/objects/problem/a3434be5bd7f8c91eb328c0bded8ab3c462ac99af6bd2a5e05bafb10d234b6d7.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-03/import/objects/problem/b4677d3125e551607a0427f8a9692820d38de47d3e52d18387890d1d6e408c76.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-03/import/objects/problem/b63b160504c38f56dab76722b3f97fd6de842c1c7efa027f67698951907c2dc5.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-03/import/objects/problem/c8fdaab732feda0e5822281809bb154c1babef61771fd5939d11c6bcb2317557.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-03/import/objects/problem/e6de9c00460c98a1a93d070f1d17e3bb7bcb442d3d2b22dd2b17906bfedc5578.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-03/import/objects/problem/f15f8a7a76b727cffcf0c13a75712d862c48ae141d058cfdb350c347bc023c75.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-03/import/report.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-03/import/residue.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-03/import/side_table.json`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-03/use-table/USE_TABLE.md`
- `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-03/use-table/use_table.json`

### `experiments/analyses/B001-arm-inventory-2026-09-14` (2 files)

- `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md`
- `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json`

### `experiments/diagnostics/C001-contrast-triple` (1912 files)

- `experiments/diagnostics/C001-contrast-triple/NOTES.md`
- `experiments/diagnostics/C001-contrast-triple/PLAN.md`
- `experiments/diagnostics/C001-contrast-triple/RECODING_TABLE.md`
- `experiments/diagnostics/C001-contrast-triple/build/build_material.py`
- `experiments/diagnostics/C001-contrast-triple/build/build_occurrence02_material.py`
- `experiments/diagnostics/C001-contrast-triple/build/recoding_units.py`
- `experiments/diagnostics/C001-contrast-triple/material-occurrence-02.json`
- `experiments/diagnostics/C001-contrast-triple/material.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/COMPARISON.md`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/RECODING_TABLE.md`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/deepseek-flash/fcl/carrier/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/deepseek-flash/fcl/carrier/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/deepseek-flash/fcl/carrier/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/deepseek-flash/fcl/carrier/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/deepseek-flash/fcl/control/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/deepseek-flash/fcl/control/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/deepseek-flash/fcl/recoding/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/deepseek-flash/fcl/recoding/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/deepseek-flash/fcl/recoding/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/deepseek-flash/prose/carrier/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/deepseek-flash/prose/carrier/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/deepseek-flash/prose/carrier/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/deepseek-flash/prose/carrier/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/deepseek-flash/prose/carrier/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/deepseek-flash/prose/control/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/deepseek-flash/prose/control/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/deepseek-flash/prose/control/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/deepseek-flash/prose/control/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/deepseek-flash/prose/control/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/deepseek-flash/prose/original/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/deepseek-flash/prose/original/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/deepseek-flash/prose/original/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/deepseek-flash/prose/original/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/deepseek-flash/prose/original/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/deepseek-flash/prose/recoding/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/deepseek-flash/prose/recoding/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/deepseek-flash/prose/recoding/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/deepseek-flash/prose/recoding/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/deepseek-flash/prose/recoding/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gemma4-31b/fcl/carrier/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gemma4-31b/fcl/carrier/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gemma4-31b/fcl/carrier/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gemma4-31b/fcl/carrier/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gemma4-31b/fcl/carrier/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gemma4-31b/fcl/control/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gemma4-31b/fcl/control/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gemma4-31b/fcl/control/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gemma4-31b/fcl/control/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gemma4-31b/fcl/control/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gemma4-31b/fcl/original/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gemma4-31b/fcl/original/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gemma4-31b/fcl/original/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gemma4-31b/fcl/original/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gemma4-31b/fcl/original/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gemma4-31b/fcl/recoding/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gemma4-31b/fcl/recoding/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gemma4-31b/fcl/recoding/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gemma4-31b/fcl/recoding/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gemma4-31b/fcl/recoding/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gemma4-31b/prose/carrier/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gemma4-31b/prose/carrier/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gemma4-31b/prose/carrier/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gemma4-31b/prose/carrier/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gemma4-31b/prose/carrier/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gemma4-31b/prose/control/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gemma4-31b/prose/control/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gemma4-31b/prose/control/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gemma4-31b/prose/control/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gemma4-31b/prose/control/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gemma4-31b/prose/original/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gemma4-31b/prose/original/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gemma4-31b/prose/original/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gemma4-31b/prose/original/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gemma4-31b/prose/original/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gemma4-31b/prose/recoding/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gemma4-31b/prose/recoding/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gemma4-31b/prose/recoding/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gemma4-31b/prose/recoding/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gemma4-31b/prose/recoding/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-glm-5.3/fcl/carrier/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-glm-5.3/fcl/carrier/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-glm-5.3/fcl/carrier/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-glm-5.3/fcl/carrier/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-glm-5.3/fcl/carrier/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-glm-5.3/fcl/control/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-glm-5.3/fcl/control/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-glm-5.3/fcl/control/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-glm-5.3/fcl/control/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-glm-5.3/fcl/control/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-glm-5.3/fcl/original/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-glm-5.3/fcl/original/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-glm-5.3/fcl/original/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-glm-5.3/fcl/original/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-glm-5.3/fcl/original/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-glm-5.3/fcl/recoding/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-glm-5.3/fcl/recoding/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-glm-5.3/fcl/recoding/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-glm-5.3/fcl/recoding/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-glm-5.3/fcl/recoding/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-glm-5.3/prose/carrier/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-glm-5.3/prose/carrier/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-glm-5.3/prose/carrier/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-glm-5.3/prose/carrier/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-glm-5.3/prose/carrier/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-glm-5.3/prose/control/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-glm-5.3/prose/control/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-glm-5.3/prose/control/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-glm-5.3/prose/control/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-glm-5.3/prose/control/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-glm-5.3/prose/original/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-glm-5.3/prose/original/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-glm-5.3/prose/original/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-glm-5.3/prose/original/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-glm-5.3/prose/original/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-glm-5.3/prose/recoding/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-glm-5.3/prose/recoding/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-glm-5.3/prose/recoding/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-glm-5.3/prose/recoding/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-glm-5.3/prose/recoding/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gpt-oss-120b/fcl/carrier/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gpt-oss-120b/fcl/carrier/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gpt-oss-120b/fcl/carrier/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gpt-oss-120b/fcl/carrier/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gpt-oss-120b/fcl/carrier/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gpt-oss-120b/fcl/control/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gpt-oss-120b/fcl/control/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gpt-oss-120b/fcl/control/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gpt-oss-120b/fcl/control/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gpt-oss-120b/fcl/control/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gpt-oss-120b/fcl/original/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gpt-oss-120b/fcl/original/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gpt-oss-120b/fcl/original/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gpt-oss-120b/fcl/original/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gpt-oss-120b/fcl/original/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gpt-oss-120b/fcl/recoding/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gpt-oss-120b/fcl/recoding/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gpt-oss-120b/fcl/recoding/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gpt-oss-120b/fcl/recoding/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gpt-oss-120b/fcl/recoding/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gpt-oss-120b/prose/carrier/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gpt-oss-120b/prose/carrier/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gpt-oss-120b/prose/carrier/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gpt-oss-120b/prose/carrier/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gpt-oss-120b/prose/carrier/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gpt-oss-120b/prose/control/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gpt-oss-120b/prose/control/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gpt-oss-120b/prose/control/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gpt-oss-120b/prose/control/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gpt-oss-120b/prose/control/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gpt-oss-120b/prose/original/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gpt-oss-120b/prose/original/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gpt-oss-120b/prose/original/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gpt-oss-120b/prose/original/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gpt-oss-120b/prose/original/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gpt-oss-120b/prose/recoding/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gpt-oss-120b/prose/recoding/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gpt-oss-120b/prose/recoding/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gpt-oss-120b/prose/recoding/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-gpt-oss-120b/prose/recoding/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-kimi-k3/fcl/carrier/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-kimi-k3/fcl/carrier/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-kimi-k3/fcl/carrier/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-kimi-k3/fcl/carrier/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-kimi-k3/fcl/carrier/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-kimi-k3/fcl/control/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-kimi-k3/fcl/control/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-kimi-k3/fcl/control/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-kimi-k3/fcl/control/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-kimi-k3/fcl/control/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-kimi-k3/fcl/original/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-kimi-k3/fcl/original/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-kimi-k3/fcl/original/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-kimi-k3/fcl/original/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-kimi-k3/fcl/original/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-kimi-k3/fcl/recoding/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-kimi-k3/fcl/recoding/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-kimi-k3/fcl/recoding/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-kimi-k3/fcl/recoding/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-kimi-k3/fcl/recoding/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-kimi-k3/prose/carrier/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-kimi-k3/prose/carrier/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-kimi-k3/prose/carrier/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-kimi-k3/prose/carrier/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-kimi-k3/prose/carrier/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-kimi-k3/prose/control/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-kimi-k3/prose/control/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-kimi-k3/prose/control/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-kimi-k3/prose/control/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-kimi-k3/prose/control/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-kimi-k3/prose/original/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-kimi-k3/prose/original/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-kimi-k3/prose/original/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-kimi-k3/prose/original/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-kimi-k3/prose/original/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-kimi-k3/prose/recoding/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-kimi-k3/prose/recoding/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-kimi-k3/prose/recoding/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-kimi-k3/prose/recoding/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-kimi-k3/prose/recoding/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-qwen3.5-397b/fcl/carrier/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-qwen3.5-397b/fcl/carrier/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-qwen3.5-397b/fcl/carrier/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-qwen3.5-397b/fcl/carrier/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-qwen3.5-397b/fcl/carrier/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-qwen3.5-397b/fcl/control/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-qwen3.5-397b/fcl/control/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-qwen3.5-397b/fcl/control/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-qwen3.5-397b/fcl/control/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-qwen3.5-397b/fcl/control/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-qwen3.5-397b/fcl/original/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-qwen3.5-397b/fcl/original/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-qwen3.5-397b/fcl/original/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-qwen3.5-397b/fcl/original/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-qwen3.5-397b/fcl/original/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-qwen3.5-397b/fcl/recoding/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-qwen3.5-397b/fcl/recoding/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-qwen3.5-397b/fcl/recoding/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-qwen3.5-397b/fcl/recoding/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-qwen3.5-397b/fcl/recoding/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-qwen3.5-397b/prose/carrier/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-qwen3.5-397b/prose/carrier/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-qwen3.5-397b/prose/carrier/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-qwen3.5-397b/prose/carrier/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-qwen3.5-397b/prose/carrier/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-qwen3.5-397b/prose/control/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-qwen3.5-397b/prose/control/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-qwen3.5-397b/prose/control/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-qwen3.5-397b/prose/control/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-qwen3.5-397b/prose/control/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-qwen3.5-397b/prose/original/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-qwen3.5-397b/prose/original/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-qwen3.5-397b/prose/original/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-qwen3.5-397b/prose/original/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-qwen3.5-397b/prose/original/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-qwen3.5-397b/prose/recoding/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-qwen3.5-397b/prose/recoding/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-qwen3.5-397b/prose/recoding/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-qwen3.5-397b/prose/recoding/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/artifacts/ollama-qwen3.5-397b/prose/recoding/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/deepseek-flash/fcl/carrier/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/deepseek-flash/fcl/carrier/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/deepseek-flash/fcl/carrier/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/deepseek-flash/fcl/carrier/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/deepseek-flash/fcl/carrier/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/deepseek-flash/fcl/control/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/deepseek-flash/fcl/control/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/deepseek-flash/fcl/control/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/deepseek-flash/fcl/control/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/deepseek-flash/fcl/control/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/deepseek-flash/fcl/original/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/deepseek-flash/fcl/original/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/deepseek-flash/fcl/original/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/deepseek-flash/fcl/original/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/deepseek-flash/fcl/original/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/deepseek-flash/fcl/recoding/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/deepseek-flash/fcl/recoding/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/deepseek-flash/fcl/recoding/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/deepseek-flash/fcl/recoding/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/deepseek-flash/fcl/recoding/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/deepseek-flash/prose/carrier/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/deepseek-flash/prose/carrier/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/deepseek-flash/prose/carrier/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/deepseek-flash/prose/carrier/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/deepseek-flash/prose/carrier/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/deepseek-flash/prose/control/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/deepseek-flash/prose/control/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/deepseek-flash/prose/control/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/deepseek-flash/prose/control/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/deepseek-flash/prose/control/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/deepseek-flash/prose/original/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/deepseek-flash/prose/original/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/deepseek-flash/prose/original/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/deepseek-flash/prose/original/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/deepseek-flash/prose/original/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/deepseek-flash/prose/recoding/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/deepseek-flash/prose/recoding/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/deepseek-flash/prose/recoding/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/deepseek-flash/prose/recoding/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/deepseek-flash/prose/recoding/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gemma4-31b/fcl/carrier/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gemma4-31b/fcl/carrier/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gemma4-31b/fcl/carrier/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gemma4-31b/fcl/carrier/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gemma4-31b/fcl/carrier/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gemma4-31b/fcl/control/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gemma4-31b/fcl/control/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gemma4-31b/fcl/control/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gemma4-31b/fcl/control/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gemma4-31b/fcl/control/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gemma4-31b/fcl/original/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gemma4-31b/fcl/original/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gemma4-31b/fcl/original/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gemma4-31b/fcl/original/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gemma4-31b/fcl/original/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gemma4-31b/fcl/recoding/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gemma4-31b/fcl/recoding/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gemma4-31b/fcl/recoding/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gemma4-31b/fcl/recoding/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gemma4-31b/fcl/recoding/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gemma4-31b/prose/carrier/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gemma4-31b/prose/carrier/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gemma4-31b/prose/carrier/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gemma4-31b/prose/carrier/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gemma4-31b/prose/carrier/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gemma4-31b/prose/control/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gemma4-31b/prose/control/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gemma4-31b/prose/control/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gemma4-31b/prose/control/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gemma4-31b/prose/control/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gemma4-31b/prose/original/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gemma4-31b/prose/original/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gemma4-31b/prose/original/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gemma4-31b/prose/original/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gemma4-31b/prose/original/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gemma4-31b/prose/recoding/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gemma4-31b/prose/recoding/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gemma4-31b/prose/recoding/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gemma4-31b/prose/recoding/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gemma4-31b/prose/recoding/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-glm-5.3/fcl/carrier/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-glm-5.3/fcl/carrier/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-glm-5.3/fcl/carrier/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-glm-5.3/fcl/carrier/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-glm-5.3/fcl/carrier/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-glm-5.3/fcl/control/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-glm-5.3/fcl/control/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-glm-5.3/fcl/control/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-glm-5.3/fcl/control/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-glm-5.3/fcl/control/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-glm-5.3/fcl/original/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-glm-5.3/fcl/original/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-glm-5.3/fcl/original/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-glm-5.3/fcl/original/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-glm-5.3/fcl/original/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-glm-5.3/fcl/recoding/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-glm-5.3/fcl/recoding/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-glm-5.3/fcl/recoding/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-glm-5.3/fcl/recoding/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-glm-5.3/fcl/recoding/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-glm-5.3/prose/carrier/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-glm-5.3/prose/carrier/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-glm-5.3/prose/carrier/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-glm-5.3/prose/carrier/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-glm-5.3/prose/carrier/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-glm-5.3/prose/control/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-glm-5.3/prose/control/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-glm-5.3/prose/control/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-glm-5.3/prose/control/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-glm-5.3/prose/control/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-glm-5.3/prose/original/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-glm-5.3/prose/original/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-glm-5.3/prose/original/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-glm-5.3/prose/original/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-glm-5.3/prose/original/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-glm-5.3/prose/recoding/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-glm-5.3/prose/recoding/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-glm-5.3/prose/recoding/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-glm-5.3/prose/recoding/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-glm-5.3/prose/recoding/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gpt-oss-120b/fcl/carrier/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gpt-oss-120b/fcl/carrier/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gpt-oss-120b/fcl/carrier/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gpt-oss-120b/fcl/carrier/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gpt-oss-120b/fcl/carrier/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gpt-oss-120b/fcl/control/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gpt-oss-120b/fcl/control/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gpt-oss-120b/fcl/control/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gpt-oss-120b/fcl/control/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gpt-oss-120b/fcl/control/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gpt-oss-120b/fcl/original/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gpt-oss-120b/fcl/original/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gpt-oss-120b/fcl/original/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gpt-oss-120b/fcl/original/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gpt-oss-120b/fcl/original/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gpt-oss-120b/fcl/recoding/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gpt-oss-120b/fcl/recoding/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gpt-oss-120b/fcl/recoding/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gpt-oss-120b/fcl/recoding/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gpt-oss-120b/fcl/recoding/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gpt-oss-120b/prose/carrier/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gpt-oss-120b/prose/carrier/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gpt-oss-120b/prose/carrier/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gpt-oss-120b/prose/carrier/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gpt-oss-120b/prose/carrier/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gpt-oss-120b/prose/control/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gpt-oss-120b/prose/control/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gpt-oss-120b/prose/control/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gpt-oss-120b/prose/control/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gpt-oss-120b/prose/control/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gpt-oss-120b/prose/original/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gpt-oss-120b/prose/original/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gpt-oss-120b/prose/original/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gpt-oss-120b/prose/original/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gpt-oss-120b/prose/original/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gpt-oss-120b/prose/recoding/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gpt-oss-120b/prose/recoding/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gpt-oss-120b/prose/recoding/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gpt-oss-120b/prose/recoding/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-gpt-oss-120b/prose/recoding/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-kimi-k3/fcl/carrier/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-kimi-k3/fcl/carrier/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-kimi-k3/fcl/carrier/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-kimi-k3/fcl/carrier/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-kimi-k3/fcl/carrier/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-kimi-k3/fcl/control/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-kimi-k3/fcl/control/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-kimi-k3/fcl/control/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-kimi-k3/fcl/control/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-kimi-k3/fcl/control/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-kimi-k3/fcl/original/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-kimi-k3/fcl/original/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-kimi-k3/fcl/original/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-kimi-k3/fcl/original/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-kimi-k3/fcl/original/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-kimi-k3/fcl/recoding/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-kimi-k3/fcl/recoding/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-kimi-k3/fcl/recoding/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-kimi-k3/fcl/recoding/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-kimi-k3/fcl/recoding/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-kimi-k3/prose/carrier/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-kimi-k3/prose/carrier/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-kimi-k3/prose/carrier/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-kimi-k3/prose/carrier/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-kimi-k3/prose/carrier/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-kimi-k3/prose/control/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-kimi-k3/prose/control/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-kimi-k3/prose/control/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-kimi-k3/prose/control/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-kimi-k3/prose/control/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-kimi-k3/prose/original/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-kimi-k3/prose/original/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-kimi-k3/prose/original/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-kimi-k3/prose/original/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-kimi-k3/prose/original/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-kimi-k3/prose/recoding/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-kimi-k3/prose/recoding/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-kimi-k3/prose/recoding/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-kimi-k3/prose/recoding/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-kimi-k3/prose/recoding/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-qwen3.5-397b/fcl/carrier/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-qwen3.5-397b/fcl/carrier/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-qwen3.5-397b/fcl/carrier/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-qwen3.5-397b/fcl/carrier/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-qwen3.5-397b/fcl/carrier/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-qwen3.5-397b/fcl/control/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-qwen3.5-397b/fcl/control/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-qwen3.5-397b/fcl/control/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-qwen3.5-397b/fcl/control/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-qwen3.5-397b/fcl/control/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-qwen3.5-397b/fcl/original/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-qwen3.5-397b/fcl/original/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-qwen3.5-397b/fcl/original/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-qwen3.5-397b/fcl/original/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-qwen3.5-397b/fcl/original/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-qwen3.5-397b/fcl/recoding/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-qwen3.5-397b/fcl/recoding/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-qwen3.5-397b/fcl/recoding/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-qwen3.5-397b/fcl/recoding/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-qwen3.5-397b/fcl/recoding/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-qwen3.5-397b/prose/carrier/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-qwen3.5-397b/prose/carrier/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-qwen3.5-397b/prose/carrier/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-qwen3.5-397b/prose/carrier/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-qwen3.5-397b/prose/carrier/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-qwen3.5-397b/prose/control/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-qwen3.5-397b/prose/control/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-qwen3.5-397b/prose/control/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-qwen3.5-397b/prose/control/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-qwen3.5-397b/prose/control/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-qwen3.5-397b/prose/original/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-qwen3.5-397b/prose/original/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-qwen3.5-397b/prose/original/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-qwen3.5-397b/prose/original/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-qwen3.5-397b/prose/original/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-qwen3.5-397b/prose/recoding/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-qwen3.5-397b/prose/recoding/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-qwen3.5-397b/prose/recoding/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-qwen3.5-397b/prose/recoding/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/attempts/ollama-qwen3.5-397b/prose/recoding/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/audit.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/briefs/fcl/carrier.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/briefs/fcl/control.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/briefs/fcl/original.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/briefs/fcl/recoding.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/briefs/prose/carrier.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/briefs/prose/control.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/briefs/prose/original.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/briefs/prose/recoding.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/comparison.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/juxtaposition/deepseek-flash__fcl.md`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/juxtaposition/deepseek-flash__prose.md`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/juxtaposition/ollama-gemma4-31b__fcl.md`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/juxtaposition/ollama-gemma4-31b__prose.md`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/juxtaposition/ollama-glm-5.3__fcl.md`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/juxtaposition/ollama-glm-5.3__prose.md`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/juxtaposition/ollama-gpt-oss-120b__fcl.md`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/juxtaposition/ollama-gpt-oss-120b__prose.md`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/juxtaposition/ollama-kimi-k3__fcl.md`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/juxtaposition/ollama-kimi-k3__prose.md`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/juxtaposition/ollama-qwen3.5-397b__fcl.md`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/juxtaposition/ollama-qwen3.5-397b__prose.md`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/plan.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/preflight.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/fcl/carrier/rep1/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/fcl/carrier/rep1/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/fcl/carrier/rep2/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/fcl/carrier/rep2/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/fcl/carrier/rep3/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/fcl/carrier/rep3/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/fcl/carrier/rep4/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/fcl/carrier/rep4/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/fcl/carrier/rep5/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/fcl/carrier/rep5/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/fcl/control/rep1/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/fcl/control/rep1/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/fcl/control/rep2/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/fcl/control/rep2/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/fcl/control/rep3/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/fcl/control/rep3/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/fcl/control/rep4/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/fcl/control/rep4/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/fcl/control/rep5/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/fcl/control/rep5/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/fcl/original/rep1/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/fcl/original/rep1/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/fcl/original/rep2/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/fcl/original/rep2/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/fcl/original/rep3/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/fcl/original/rep3/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/fcl/original/rep4/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/fcl/original/rep4/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/fcl/original/rep5/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/fcl/original/rep5/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/fcl/recoding/rep1/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/fcl/recoding/rep1/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/fcl/recoding/rep2/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/fcl/recoding/rep2/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/fcl/recoding/rep3/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/fcl/recoding/rep3/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/fcl/recoding/rep4/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/fcl/recoding/rep4/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/fcl/recoding/rep5/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/fcl/recoding/rep5/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/prose/carrier/rep1/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/prose/carrier/rep1/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/prose/carrier/rep2/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/prose/carrier/rep2/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/prose/carrier/rep3/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/prose/carrier/rep3/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/prose/carrier/rep4/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/prose/carrier/rep4/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/prose/carrier/rep5/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/prose/carrier/rep5/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/prose/control/rep1/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/prose/control/rep1/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/prose/control/rep2/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/prose/control/rep2/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/prose/control/rep3/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/prose/control/rep3/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/prose/control/rep4/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/prose/control/rep4/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/prose/control/rep5/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/prose/control/rep5/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/prose/original/rep1/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/prose/original/rep1/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/prose/original/rep2/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/prose/original/rep2/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/prose/original/rep3/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/prose/original/rep3/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/prose/original/rep4/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/prose/original/rep4/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/prose/original/rep5/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/prose/original/rep5/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/prose/recoding/rep1/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/prose/recoding/rep1/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/prose/recoding/rep2/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/prose/recoding/rep2/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/prose/recoding/rep3/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/prose/recoding/rep3/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/prose/recoding/rep4/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/prose/recoding/rep4/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/prose/recoding/rep5/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/deepseek-flash/prose/recoding/rep5/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/fcl/carrier/rep1/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/fcl/carrier/rep1/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/fcl/carrier/rep2/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/fcl/carrier/rep2/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/fcl/carrier/rep3/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/fcl/carrier/rep3/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/fcl/carrier/rep4/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/fcl/carrier/rep4/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/fcl/carrier/rep5/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/fcl/carrier/rep5/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/fcl/control/rep1/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/fcl/control/rep1/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/fcl/control/rep2/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/fcl/control/rep2/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/fcl/control/rep3/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/fcl/control/rep3/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/fcl/control/rep4/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/fcl/control/rep4/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/fcl/control/rep5/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/fcl/control/rep5/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/fcl/original/rep1/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/fcl/original/rep1/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/fcl/original/rep2/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/fcl/original/rep2/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/fcl/original/rep3/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/fcl/original/rep3/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/fcl/original/rep4/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/fcl/original/rep4/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/fcl/original/rep5/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/fcl/original/rep5/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/fcl/recoding/rep1/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/fcl/recoding/rep1/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/fcl/recoding/rep2/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/fcl/recoding/rep2/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/fcl/recoding/rep3/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/fcl/recoding/rep3/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/fcl/recoding/rep4/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/fcl/recoding/rep4/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/fcl/recoding/rep5/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/fcl/recoding/rep5/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/prose/carrier/rep1/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/prose/carrier/rep1/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/prose/carrier/rep2/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/prose/carrier/rep2/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/prose/carrier/rep3/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/prose/carrier/rep3/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/prose/carrier/rep4/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/prose/carrier/rep4/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/prose/carrier/rep5/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/prose/carrier/rep5/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/prose/control/rep1/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/prose/control/rep1/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/prose/control/rep2/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/prose/control/rep2/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/prose/control/rep3/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/prose/control/rep3/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/prose/control/rep4/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/prose/control/rep4/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/prose/control/rep5/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/prose/control/rep5/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/prose/original/rep1/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/prose/original/rep1/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/prose/original/rep2/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/prose/original/rep2/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/prose/original/rep3/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/prose/original/rep3/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/prose/original/rep4/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/prose/original/rep4/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/prose/original/rep5/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/prose/original/rep5/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/prose/recoding/rep1/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/prose/recoding/rep1/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/prose/recoding/rep2/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/prose/recoding/rep2/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/prose/recoding/rep3/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/prose/recoding/rep3/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/prose/recoding/rep4/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/prose/recoding/rep4/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/prose/recoding/rep5/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gemma4-31b/prose/recoding/rep5/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/fcl/carrier/rep1/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/fcl/carrier/rep1/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/fcl/carrier/rep2/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/fcl/carrier/rep2/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/fcl/carrier/rep3/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/fcl/carrier/rep3/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/fcl/carrier/rep4/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/fcl/carrier/rep4/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/fcl/carrier/rep5/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/fcl/carrier/rep5/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/fcl/control/rep1/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/fcl/control/rep1/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/fcl/control/rep2/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/fcl/control/rep2/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/fcl/control/rep3/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/fcl/control/rep3/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/fcl/control/rep4/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/fcl/control/rep4/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/fcl/control/rep5/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/fcl/control/rep5/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/fcl/original/rep1/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/fcl/original/rep1/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/fcl/original/rep2/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/fcl/original/rep2/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/fcl/original/rep3/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/fcl/original/rep3/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/fcl/original/rep4/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/fcl/original/rep4/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/fcl/original/rep5/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/fcl/original/rep5/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/fcl/recoding/rep1/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/fcl/recoding/rep1/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/fcl/recoding/rep2/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/fcl/recoding/rep2/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/fcl/recoding/rep3/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/fcl/recoding/rep3/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/fcl/recoding/rep4/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/fcl/recoding/rep4/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/fcl/recoding/rep5/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/fcl/recoding/rep5/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/prose/carrier/rep1/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/prose/carrier/rep1/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/prose/carrier/rep2/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/prose/carrier/rep2/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/prose/carrier/rep3/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/prose/carrier/rep3/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/prose/carrier/rep4/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/prose/carrier/rep4/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/prose/carrier/rep5/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/prose/carrier/rep5/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/prose/control/rep1/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/prose/control/rep1/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/prose/control/rep2/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/prose/control/rep2/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/prose/control/rep3/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/prose/control/rep3/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/prose/control/rep4/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/prose/control/rep4/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/prose/control/rep5/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/prose/control/rep5/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/prose/original/rep1/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/prose/original/rep1/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/prose/original/rep2/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/prose/original/rep2/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/prose/original/rep3/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/prose/original/rep3/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/prose/original/rep4/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/prose/original/rep4/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/prose/original/rep5/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/prose/original/rep5/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/prose/recoding/rep1/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/prose/recoding/rep1/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/prose/recoding/rep2/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/prose/recoding/rep2/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/prose/recoding/rep3/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/prose/recoding/rep3/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/prose/recoding/rep4/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/prose/recoding/rep4/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/prose/recoding/rep5/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-glm-5.3/prose/recoding/rep5/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/fcl/carrier/rep1/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/fcl/carrier/rep1/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/fcl/carrier/rep2/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/fcl/carrier/rep2/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/fcl/carrier/rep3/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/fcl/carrier/rep3/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/fcl/carrier/rep4/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/fcl/carrier/rep4/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/fcl/carrier/rep5/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/fcl/carrier/rep5/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/fcl/control/rep1/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/fcl/control/rep1/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/fcl/control/rep2/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/fcl/control/rep2/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/fcl/control/rep3/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/fcl/control/rep3/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/fcl/control/rep4/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/fcl/control/rep4/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/fcl/control/rep5/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/fcl/control/rep5/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/fcl/original/rep1/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/fcl/original/rep1/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/fcl/original/rep2/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/fcl/original/rep2/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/fcl/original/rep3/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/fcl/original/rep3/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/fcl/original/rep4/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/fcl/original/rep4/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/fcl/original/rep5/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/fcl/original/rep5/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/fcl/recoding/rep1/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/fcl/recoding/rep1/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/fcl/recoding/rep2/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/fcl/recoding/rep2/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/fcl/recoding/rep3/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/fcl/recoding/rep3/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/fcl/recoding/rep4/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/fcl/recoding/rep4/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/fcl/recoding/rep5/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/fcl/recoding/rep5/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/prose/carrier/rep1/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/prose/carrier/rep1/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/prose/carrier/rep2/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/prose/carrier/rep2/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/prose/carrier/rep3/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/prose/carrier/rep3/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/prose/carrier/rep4/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/prose/carrier/rep4/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/prose/carrier/rep5/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/prose/carrier/rep5/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/prose/control/rep1/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/prose/control/rep1/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/prose/control/rep2/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/prose/control/rep2/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/prose/control/rep3/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/prose/control/rep3/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/prose/control/rep4/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/prose/control/rep4/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/prose/control/rep5/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/prose/control/rep5/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/prose/original/rep1/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/prose/original/rep1/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/prose/original/rep2/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/prose/original/rep2/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/prose/original/rep3/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/prose/original/rep3/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/prose/original/rep4/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/prose/original/rep4/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/prose/original/rep5/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/prose/original/rep5/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/prose/recoding/rep1/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/prose/recoding/rep1/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/prose/recoding/rep2/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/prose/recoding/rep2/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/prose/recoding/rep3/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/prose/recoding/rep3/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/prose/recoding/rep4/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/prose/recoding/rep4/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/prose/recoding/rep5/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-gpt-oss-120b/prose/recoding/rep5/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/fcl/carrier/rep1/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/fcl/carrier/rep1/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/fcl/carrier/rep2/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/fcl/carrier/rep2/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/fcl/carrier/rep3/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/fcl/carrier/rep3/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/fcl/carrier/rep4/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/fcl/carrier/rep4/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/fcl/carrier/rep5/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/fcl/carrier/rep5/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/fcl/control/rep1/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/fcl/control/rep1/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/fcl/control/rep2/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/fcl/control/rep2/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/fcl/control/rep3/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/fcl/control/rep3/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/fcl/control/rep4/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/fcl/control/rep4/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/fcl/control/rep5/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/fcl/control/rep5/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/fcl/original/rep1/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/fcl/original/rep1/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/fcl/original/rep2/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/fcl/original/rep2/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/fcl/original/rep3/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/fcl/original/rep3/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/fcl/original/rep4/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/fcl/original/rep4/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/fcl/original/rep5/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/fcl/original/rep5/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/fcl/recoding/rep1/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/fcl/recoding/rep1/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/fcl/recoding/rep2/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/fcl/recoding/rep2/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/fcl/recoding/rep3/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/fcl/recoding/rep3/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/fcl/recoding/rep4/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/fcl/recoding/rep4/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/fcl/recoding/rep5/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/fcl/recoding/rep5/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/prose/carrier/rep1/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/prose/carrier/rep1/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/prose/carrier/rep2/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/prose/carrier/rep2/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/prose/carrier/rep3/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/prose/carrier/rep3/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/prose/carrier/rep4/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/prose/carrier/rep4/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/prose/carrier/rep5/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/prose/carrier/rep5/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/prose/control/rep1/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/prose/control/rep1/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/prose/control/rep2/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/prose/control/rep2/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/prose/control/rep3/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/prose/control/rep3/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/prose/control/rep4/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/prose/control/rep4/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/prose/control/rep5/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/prose/control/rep5/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/prose/original/rep1/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/prose/original/rep1/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/prose/original/rep2/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/prose/original/rep2/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/prose/original/rep3/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/prose/original/rep3/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/prose/original/rep4/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/prose/original/rep4/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/prose/original/rep5/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/prose/original/rep5/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/prose/recoding/rep1/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/prose/recoding/rep1/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/prose/recoding/rep2/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/prose/recoding/rep2/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/prose/recoding/rep3/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/prose/recoding/rep3/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/prose/recoding/rep4/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/prose/recoding/rep4/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/prose/recoding/rep5/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-kimi-k3/prose/recoding/rep5/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/fcl/carrier/rep1/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/fcl/carrier/rep1/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/fcl/carrier/rep2/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/fcl/carrier/rep2/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/fcl/carrier/rep3/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/fcl/carrier/rep3/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/fcl/carrier/rep4/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/fcl/carrier/rep4/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/fcl/carrier/rep5/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/fcl/carrier/rep5/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/fcl/control/rep1/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/fcl/control/rep1/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/fcl/control/rep2/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/fcl/control/rep2/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/fcl/control/rep3/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/fcl/control/rep3/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/fcl/control/rep4/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/fcl/control/rep4/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/fcl/control/rep5/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/fcl/control/rep5/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/fcl/original/rep1/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/fcl/original/rep1/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/fcl/original/rep2/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/fcl/original/rep2/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/fcl/original/rep3/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/fcl/original/rep3/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/fcl/original/rep4/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/fcl/original/rep4/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/fcl/original/rep5/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/fcl/original/rep5/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/fcl/recoding/rep1/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/fcl/recoding/rep1/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/fcl/recoding/rep2/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/fcl/recoding/rep2/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/fcl/recoding/rep3/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/fcl/recoding/rep3/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/fcl/recoding/rep4/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/fcl/recoding/rep4/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/fcl/recoding/rep5/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/fcl/recoding/rep5/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/prose/carrier/rep1/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/prose/carrier/rep1/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/prose/carrier/rep2/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/prose/carrier/rep2/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/prose/carrier/rep3/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/prose/carrier/rep3/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/prose/carrier/rep4/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/prose/carrier/rep4/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/prose/carrier/rep5/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/prose/carrier/rep5/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/prose/control/rep1/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/prose/control/rep1/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/prose/control/rep2/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/prose/control/rep2/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/prose/control/rep3/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/prose/control/rep3/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/prose/control/rep4/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/prose/control/rep4/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/prose/control/rep5/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/prose/control/rep5/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/prose/original/rep1/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/prose/original/rep1/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/prose/original/rep2/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/prose/original/rep2/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/prose/original/rep3/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/prose/original/rep3/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/prose/original/rep4/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/prose/original/rep4/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/prose/original/rep5/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/prose/original/rep5/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/prose/recoding/rep1/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/prose/recoding/rep1/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/prose/recoding/rep2/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/prose/recoding/rep2/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/prose/recoding/rep3/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/prose/recoding/rep3/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/prose/recoding/rep4/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/prose/recoding/rep4/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/prose/recoding/rep5/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/provider/ollama-qwen3.5-397b/prose/recoding/rep5/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/deepseek-flash/fcl/carrier/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/deepseek-flash/fcl/carrier/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/deepseek-flash/fcl/carrier/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/deepseek-flash/fcl/carrier/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/deepseek-flash/fcl/carrier/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/deepseek-flash/fcl/control/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/deepseek-flash/fcl/control/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/deepseek-flash/fcl/control/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/deepseek-flash/fcl/control/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/deepseek-flash/fcl/control/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/deepseek-flash/fcl/original/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/deepseek-flash/fcl/original/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/deepseek-flash/fcl/original/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/deepseek-flash/fcl/original/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/deepseek-flash/fcl/original/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/deepseek-flash/fcl/recoding/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/deepseek-flash/fcl/recoding/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/deepseek-flash/fcl/recoding/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/deepseek-flash/fcl/recoding/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/deepseek-flash/fcl/recoding/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/deepseek-flash/prose/carrier/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/deepseek-flash/prose/carrier/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/deepseek-flash/prose/carrier/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/deepseek-flash/prose/carrier/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/deepseek-flash/prose/carrier/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/deepseek-flash/prose/control/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/deepseek-flash/prose/control/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/deepseek-flash/prose/control/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/deepseek-flash/prose/control/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/deepseek-flash/prose/control/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/deepseek-flash/prose/original/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/deepseek-flash/prose/original/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/deepseek-flash/prose/original/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/deepseek-flash/prose/original/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/deepseek-flash/prose/original/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/deepseek-flash/prose/recoding/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/deepseek-flash/prose/recoding/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/deepseek-flash/prose/recoding/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/deepseek-flash/prose/recoding/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/deepseek-flash/prose/recoding/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gemma4-31b/fcl/carrier/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gemma4-31b/fcl/carrier/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gemma4-31b/fcl/carrier/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gemma4-31b/fcl/carrier/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gemma4-31b/fcl/carrier/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gemma4-31b/fcl/control/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gemma4-31b/fcl/control/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gemma4-31b/fcl/control/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gemma4-31b/fcl/control/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gemma4-31b/fcl/control/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gemma4-31b/fcl/original/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gemma4-31b/fcl/original/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gemma4-31b/fcl/original/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gemma4-31b/fcl/original/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gemma4-31b/fcl/original/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gemma4-31b/fcl/recoding/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gemma4-31b/fcl/recoding/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gemma4-31b/fcl/recoding/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gemma4-31b/fcl/recoding/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gemma4-31b/fcl/recoding/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gemma4-31b/prose/carrier/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gemma4-31b/prose/carrier/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gemma4-31b/prose/carrier/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gemma4-31b/prose/carrier/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gemma4-31b/prose/carrier/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gemma4-31b/prose/control/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gemma4-31b/prose/control/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gemma4-31b/prose/control/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gemma4-31b/prose/control/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gemma4-31b/prose/control/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gemma4-31b/prose/original/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gemma4-31b/prose/original/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gemma4-31b/prose/original/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gemma4-31b/prose/original/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gemma4-31b/prose/original/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gemma4-31b/prose/recoding/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gemma4-31b/prose/recoding/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gemma4-31b/prose/recoding/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gemma4-31b/prose/recoding/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gemma4-31b/prose/recoding/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-glm-5.3/fcl/carrier/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-glm-5.3/fcl/carrier/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-glm-5.3/fcl/carrier/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-glm-5.3/fcl/carrier/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-glm-5.3/fcl/carrier/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-glm-5.3/fcl/control/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-glm-5.3/fcl/control/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-glm-5.3/fcl/control/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-glm-5.3/fcl/control/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-glm-5.3/fcl/control/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-glm-5.3/fcl/original/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-glm-5.3/fcl/original/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-glm-5.3/fcl/original/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-glm-5.3/fcl/original/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-glm-5.3/fcl/original/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-glm-5.3/fcl/recoding/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-glm-5.3/fcl/recoding/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-glm-5.3/fcl/recoding/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-glm-5.3/fcl/recoding/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-glm-5.3/fcl/recoding/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-glm-5.3/prose/carrier/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-glm-5.3/prose/carrier/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-glm-5.3/prose/carrier/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-glm-5.3/prose/carrier/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-glm-5.3/prose/carrier/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-glm-5.3/prose/control/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-glm-5.3/prose/control/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-glm-5.3/prose/control/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-glm-5.3/prose/control/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-glm-5.3/prose/control/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-glm-5.3/prose/original/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-glm-5.3/prose/original/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-glm-5.3/prose/original/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-glm-5.3/prose/original/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-glm-5.3/prose/original/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-glm-5.3/prose/recoding/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-glm-5.3/prose/recoding/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-glm-5.3/prose/recoding/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-glm-5.3/prose/recoding/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-glm-5.3/prose/recoding/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gpt-oss-120b/fcl/carrier/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gpt-oss-120b/fcl/carrier/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gpt-oss-120b/fcl/carrier/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gpt-oss-120b/fcl/carrier/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gpt-oss-120b/fcl/carrier/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gpt-oss-120b/fcl/control/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gpt-oss-120b/fcl/control/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gpt-oss-120b/fcl/control/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gpt-oss-120b/fcl/control/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gpt-oss-120b/fcl/control/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gpt-oss-120b/fcl/original/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gpt-oss-120b/fcl/original/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gpt-oss-120b/fcl/original/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gpt-oss-120b/fcl/original/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gpt-oss-120b/fcl/original/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gpt-oss-120b/fcl/recoding/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gpt-oss-120b/fcl/recoding/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gpt-oss-120b/fcl/recoding/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gpt-oss-120b/fcl/recoding/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gpt-oss-120b/fcl/recoding/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gpt-oss-120b/prose/carrier/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gpt-oss-120b/prose/carrier/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gpt-oss-120b/prose/carrier/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gpt-oss-120b/prose/carrier/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gpt-oss-120b/prose/carrier/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gpt-oss-120b/prose/control/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gpt-oss-120b/prose/control/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gpt-oss-120b/prose/control/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gpt-oss-120b/prose/control/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gpt-oss-120b/prose/control/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gpt-oss-120b/prose/original/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gpt-oss-120b/prose/original/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gpt-oss-120b/prose/original/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gpt-oss-120b/prose/original/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gpt-oss-120b/prose/original/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gpt-oss-120b/prose/recoding/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gpt-oss-120b/prose/recoding/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gpt-oss-120b/prose/recoding/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gpt-oss-120b/prose/recoding/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-gpt-oss-120b/prose/recoding/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-kimi-k3/fcl/carrier/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-kimi-k3/fcl/carrier/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-kimi-k3/fcl/carrier/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-kimi-k3/fcl/carrier/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-kimi-k3/fcl/carrier/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-kimi-k3/fcl/control/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-kimi-k3/fcl/control/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-kimi-k3/fcl/control/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-kimi-k3/fcl/control/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-kimi-k3/fcl/control/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-kimi-k3/fcl/original/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-kimi-k3/fcl/original/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-kimi-k3/fcl/original/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-kimi-k3/fcl/original/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-kimi-k3/fcl/original/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-kimi-k3/fcl/recoding/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-kimi-k3/fcl/recoding/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-kimi-k3/fcl/recoding/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-kimi-k3/fcl/recoding/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-kimi-k3/fcl/recoding/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-kimi-k3/prose/carrier/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-kimi-k3/prose/carrier/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-kimi-k3/prose/carrier/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-kimi-k3/prose/carrier/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-kimi-k3/prose/carrier/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-kimi-k3/prose/control/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-kimi-k3/prose/control/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-kimi-k3/prose/control/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-kimi-k3/prose/control/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-kimi-k3/prose/control/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-kimi-k3/prose/original/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-kimi-k3/prose/original/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-kimi-k3/prose/original/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-kimi-k3/prose/original/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-kimi-k3/prose/original/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-kimi-k3/prose/recoding/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-kimi-k3/prose/recoding/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-kimi-k3/prose/recoding/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-kimi-k3/prose/recoding/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-kimi-k3/prose/recoding/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-qwen3.5-397b/fcl/carrier/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-qwen3.5-397b/fcl/carrier/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-qwen3.5-397b/fcl/carrier/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-qwen3.5-397b/fcl/carrier/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-qwen3.5-397b/fcl/carrier/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-qwen3.5-397b/fcl/control/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-qwen3.5-397b/fcl/control/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-qwen3.5-397b/fcl/control/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-qwen3.5-397b/fcl/control/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-qwen3.5-397b/fcl/control/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-qwen3.5-397b/fcl/original/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-qwen3.5-397b/fcl/original/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-qwen3.5-397b/fcl/original/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-qwen3.5-397b/fcl/original/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-qwen3.5-397b/fcl/original/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-qwen3.5-397b/fcl/recoding/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-qwen3.5-397b/fcl/recoding/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-qwen3.5-397b/fcl/recoding/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-qwen3.5-397b/fcl/recoding/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-qwen3.5-397b/fcl/recoding/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-qwen3.5-397b/prose/carrier/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-qwen3.5-397b/prose/carrier/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-qwen3.5-397b/prose/carrier/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-qwen3.5-397b/prose/carrier/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-qwen3.5-397b/prose/carrier/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-qwen3.5-397b/prose/control/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-qwen3.5-397b/prose/control/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-qwen3.5-397b/prose/control/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-qwen3.5-397b/prose/control/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-qwen3.5-397b/prose/control/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-qwen3.5-397b/prose/original/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-qwen3.5-397b/prose/original/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-qwen3.5-397b/prose/original/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-qwen3.5-397b/prose/original/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-qwen3.5-397b/prose/original/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-qwen3.5-397b/prose/recoding/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-qwen3.5-397b/prose/recoding/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-qwen3.5-397b/prose/recoding/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-qwen3.5-397b/prose/recoding/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/requests/ollama-qwen3.5-397b/prose/recoding/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/fcl/carrier/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/fcl/carrier/rep1.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/fcl/carrier/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/fcl/carrier/rep2.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/fcl/carrier/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/fcl/carrier/rep3.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/fcl/carrier/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/fcl/carrier/rep4.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/fcl/carrier/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/fcl/carrier/rep5.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/fcl/control/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/fcl/control/rep1.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/fcl/control/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/fcl/control/rep2.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/fcl/control/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/fcl/control/rep3.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/fcl/control/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/fcl/control/rep4.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/fcl/control/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/fcl/control/rep5.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/fcl/original/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/fcl/original/rep1.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/fcl/original/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/fcl/original/rep2.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/fcl/original/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/fcl/original/rep3.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/fcl/original/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/fcl/original/rep4.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/fcl/original/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/fcl/original/rep5.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/fcl/recoding/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/fcl/recoding/rep1.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/fcl/recoding/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/fcl/recoding/rep2.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/fcl/recoding/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/fcl/recoding/rep3.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/fcl/recoding/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/fcl/recoding/rep4.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/fcl/recoding/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/fcl/recoding/rep5.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/prose/carrier/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/prose/carrier/rep1.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/prose/carrier/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/prose/carrier/rep2.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/prose/carrier/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/prose/carrier/rep3.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/prose/carrier/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/prose/carrier/rep4.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/prose/carrier/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/prose/carrier/rep5.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/prose/control/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/prose/control/rep1.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/prose/control/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/prose/control/rep2.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/prose/control/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/prose/control/rep3.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/prose/control/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/prose/control/rep4.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/prose/control/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/prose/control/rep5.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/prose/original/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/prose/original/rep1.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/prose/original/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/prose/original/rep2.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/prose/original/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/prose/original/rep3.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/prose/original/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/prose/original/rep4.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/prose/original/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/prose/original/rep5.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/prose/recoding/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/prose/recoding/rep1.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/prose/recoding/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/prose/recoding/rep2.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/prose/recoding/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/prose/recoding/rep3.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/prose/recoding/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/prose/recoding/rep4.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/prose/recoding/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/deepseek-flash/prose/recoding/rep5.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/fcl/carrier/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/fcl/carrier/rep1.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/fcl/carrier/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/fcl/carrier/rep2.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/fcl/carrier/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/fcl/carrier/rep3.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/fcl/carrier/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/fcl/carrier/rep4.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/fcl/carrier/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/fcl/carrier/rep5.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/fcl/control/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/fcl/control/rep1.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/fcl/control/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/fcl/control/rep2.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/fcl/control/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/fcl/control/rep3.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/fcl/control/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/fcl/control/rep4.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/fcl/control/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/fcl/control/rep5.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/fcl/original/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/fcl/original/rep1.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/fcl/original/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/fcl/original/rep2.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/fcl/original/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/fcl/original/rep3.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/fcl/original/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/fcl/original/rep4.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/fcl/original/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/fcl/original/rep5.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/fcl/recoding/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/fcl/recoding/rep1.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/fcl/recoding/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/fcl/recoding/rep2.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/fcl/recoding/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/fcl/recoding/rep3.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/fcl/recoding/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/fcl/recoding/rep4.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/fcl/recoding/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/fcl/recoding/rep5.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/prose/carrier/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/prose/carrier/rep1.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/prose/carrier/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/prose/carrier/rep2.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/prose/carrier/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/prose/carrier/rep3.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/prose/carrier/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/prose/carrier/rep4.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/prose/carrier/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/prose/carrier/rep5.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/prose/control/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/prose/control/rep1.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/prose/control/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/prose/control/rep2.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/prose/control/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/prose/control/rep3.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/prose/control/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/prose/control/rep4.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/prose/control/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/prose/control/rep5.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/prose/original/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/prose/original/rep1.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/prose/original/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/prose/original/rep2.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/prose/original/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/prose/original/rep3.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/prose/original/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/prose/original/rep4.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/prose/original/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/prose/original/rep5.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/prose/recoding/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/prose/recoding/rep1.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/prose/recoding/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/prose/recoding/rep2.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/prose/recoding/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/prose/recoding/rep3.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/prose/recoding/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/prose/recoding/rep4.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/prose/recoding/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gemma4-31b/prose/recoding/rep5.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/fcl/carrier/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/fcl/carrier/rep1.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/fcl/carrier/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/fcl/carrier/rep2.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/fcl/carrier/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/fcl/carrier/rep3.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/fcl/carrier/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/fcl/carrier/rep4.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/fcl/carrier/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/fcl/carrier/rep5.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/fcl/control/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/fcl/control/rep1.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/fcl/control/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/fcl/control/rep2.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/fcl/control/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/fcl/control/rep3.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/fcl/control/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/fcl/control/rep4.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/fcl/control/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/fcl/control/rep5.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/fcl/original/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/fcl/original/rep1.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/fcl/original/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/fcl/original/rep2.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/fcl/original/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/fcl/original/rep3.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/fcl/original/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/fcl/original/rep4.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/fcl/original/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/fcl/original/rep5.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/fcl/recoding/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/fcl/recoding/rep1.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/fcl/recoding/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/fcl/recoding/rep2.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/fcl/recoding/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/fcl/recoding/rep3.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/fcl/recoding/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/fcl/recoding/rep4.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/fcl/recoding/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/fcl/recoding/rep5.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/prose/carrier/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/prose/carrier/rep1.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/prose/carrier/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/prose/carrier/rep2.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/prose/carrier/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/prose/carrier/rep3.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/prose/carrier/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/prose/carrier/rep4.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/prose/carrier/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/prose/carrier/rep5.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/prose/control/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/prose/control/rep1.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/prose/control/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/prose/control/rep2.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/prose/control/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/prose/control/rep3.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/prose/control/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/prose/control/rep4.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/prose/control/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/prose/control/rep5.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/prose/original/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/prose/original/rep1.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/prose/original/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/prose/original/rep2.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/prose/original/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/prose/original/rep3.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/prose/original/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/prose/original/rep4.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/prose/original/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/prose/original/rep5.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/prose/recoding/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/prose/recoding/rep1.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/prose/recoding/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/prose/recoding/rep2.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/prose/recoding/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/prose/recoding/rep3.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/prose/recoding/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/prose/recoding/rep4.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/prose/recoding/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-glm-5.3/prose/recoding/rep5.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/fcl/carrier/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/fcl/carrier/rep1.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/fcl/carrier/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/fcl/carrier/rep2.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/fcl/carrier/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/fcl/carrier/rep3.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/fcl/carrier/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/fcl/carrier/rep4.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/fcl/carrier/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/fcl/carrier/rep5.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/fcl/control/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/fcl/control/rep1.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/fcl/control/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/fcl/control/rep2.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/fcl/control/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/fcl/control/rep3.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/fcl/control/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/fcl/control/rep4.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/fcl/control/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/fcl/control/rep5.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/fcl/original/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/fcl/original/rep1.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/fcl/original/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/fcl/original/rep2.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/fcl/original/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/fcl/original/rep3.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/fcl/original/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/fcl/original/rep4.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/fcl/original/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/fcl/original/rep5.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/fcl/recoding/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/fcl/recoding/rep1.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/fcl/recoding/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/fcl/recoding/rep2.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/fcl/recoding/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/fcl/recoding/rep3.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/fcl/recoding/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/fcl/recoding/rep4.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/fcl/recoding/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/fcl/recoding/rep5.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/prose/carrier/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/prose/carrier/rep1.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/prose/carrier/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/prose/carrier/rep2.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/prose/carrier/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/prose/carrier/rep3.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/prose/carrier/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/prose/carrier/rep4.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/prose/carrier/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/prose/carrier/rep5.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/prose/control/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/prose/control/rep1.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/prose/control/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/prose/control/rep2.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/prose/control/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/prose/control/rep3.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/prose/control/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/prose/control/rep4.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/prose/control/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/prose/control/rep5.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/prose/original/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/prose/original/rep1.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/prose/original/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/prose/original/rep2.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/prose/original/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/prose/original/rep3.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/prose/original/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/prose/original/rep4.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/prose/original/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/prose/original/rep5.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/prose/recoding/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/prose/recoding/rep1.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/prose/recoding/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/prose/recoding/rep2.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/prose/recoding/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/prose/recoding/rep3.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/prose/recoding/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/prose/recoding/rep4.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/prose/recoding/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-gpt-oss-120b/prose/recoding/rep5.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/fcl/carrier/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/fcl/carrier/rep1.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/fcl/carrier/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/fcl/carrier/rep2.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/fcl/carrier/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/fcl/carrier/rep3.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/fcl/carrier/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/fcl/carrier/rep4.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/fcl/carrier/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/fcl/carrier/rep5.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/fcl/control/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/fcl/control/rep1.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/fcl/control/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/fcl/control/rep2.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/fcl/control/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/fcl/control/rep3.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/fcl/control/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/fcl/control/rep4.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/fcl/control/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/fcl/control/rep5.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/fcl/original/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/fcl/original/rep1.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/fcl/original/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/fcl/original/rep2.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/fcl/original/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/fcl/original/rep3.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/fcl/original/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/fcl/original/rep4.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/fcl/original/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/fcl/original/rep5.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/fcl/recoding/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/fcl/recoding/rep1.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/fcl/recoding/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/fcl/recoding/rep2.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/fcl/recoding/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/fcl/recoding/rep3.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/fcl/recoding/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/fcl/recoding/rep4.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/fcl/recoding/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/fcl/recoding/rep5.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/prose/carrier/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/prose/carrier/rep1.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/prose/carrier/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/prose/carrier/rep2.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/prose/carrier/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/prose/carrier/rep3.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/prose/carrier/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/prose/carrier/rep4.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/prose/carrier/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/prose/carrier/rep5.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/prose/control/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/prose/control/rep1.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/prose/control/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/prose/control/rep2.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/prose/control/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/prose/control/rep3.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/prose/control/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/prose/control/rep4.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/prose/control/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/prose/control/rep5.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/prose/original/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/prose/original/rep1.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/prose/original/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/prose/original/rep2.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/prose/original/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/prose/original/rep3.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/prose/original/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/prose/original/rep4.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/prose/original/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/prose/original/rep5.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/prose/recoding/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/prose/recoding/rep1.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/prose/recoding/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/prose/recoding/rep2.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/prose/recoding/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/prose/recoding/rep3.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/prose/recoding/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/prose/recoding/rep4.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/prose/recoding/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-kimi-k3/prose/recoding/rep5.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/fcl/carrier/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/fcl/carrier/rep1.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/fcl/carrier/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/fcl/carrier/rep2.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/fcl/carrier/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/fcl/carrier/rep3.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/fcl/carrier/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/fcl/carrier/rep4.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/fcl/carrier/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/fcl/carrier/rep5.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/fcl/control/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/fcl/control/rep1.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/fcl/control/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/fcl/control/rep2.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/fcl/control/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/fcl/control/rep3.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/fcl/control/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/fcl/control/rep4.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/fcl/control/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/fcl/control/rep5.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/fcl/original/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/fcl/original/rep1.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/fcl/original/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/fcl/original/rep2.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/fcl/original/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/fcl/original/rep3.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/fcl/original/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/fcl/original/rep4.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/fcl/original/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/fcl/original/rep5.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/fcl/recoding/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/fcl/recoding/rep1.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/fcl/recoding/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/fcl/recoding/rep2.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/fcl/recoding/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/fcl/recoding/rep3.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/fcl/recoding/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/fcl/recoding/rep4.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/fcl/recoding/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/fcl/recoding/rep5.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/prose/carrier/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/prose/carrier/rep1.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/prose/carrier/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/prose/carrier/rep2.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/prose/carrier/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/prose/carrier/rep3.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/prose/carrier/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/prose/carrier/rep4.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/prose/carrier/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/prose/carrier/rep5.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/prose/control/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/prose/control/rep1.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/prose/control/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/prose/control/rep2.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/prose/control/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/prose/control/rep3.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/prose/control/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/prose/control/rep4.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/prose/control/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/prose/control/rep5.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/prose/original/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/prose/original/rep1.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/prose/original/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/prose/original/rep2.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/prose/original/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/prose/original/rep3.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/prose/original/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/prose/original/rep4.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/prose/original/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/prose/original/rep5.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/prose/recoding/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/prose/recoding/rep1.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/prose/recoding/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/prose/recoding/rep2.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/prose/recoding/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/prose/recoding/rep3.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/prose/recoding/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/prose/recoding/rep4.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/prose/recoding/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/ollama-qwen3.5-397b/prose/recoding/rep5.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/waves/wave0001.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/waves/wave0002.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/waves/wave0003.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/waves/wave0004.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/waves/wave0005.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/waves/wave0006.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/waves/wave0007.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/waves/wave0008.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/waves/wave0009.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/waves/wave0010.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/waves/wave0011.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/waves/wave0012.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/waves/wave0013.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/waves/wave0014.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/waves/wave0015.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/waves/wave0016.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/waves/wave0017.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/waves/wave0018.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/waves/wave0019.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/waves/wave0020.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/waves/wave0021.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/waves/wave0022.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/waves/wave0023.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/waves/wave0024.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/waves/wave0025.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/waves/wave0026.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/waves/wave0027.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/waves/wave0028.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/waves/wave0029.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/waves/wave0030.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/waves/wave0031.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/waves/wave0032.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/waves/wave0033.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/waves/wave0034.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/waves/wave0035.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/waves/wave0036.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/waves/wave0037.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/waves/wave0038.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/waves/wave0039.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/waves/wave0040.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/waves/wave0041.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/waves/wave0042.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/waves/wave0043.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/waves/wave0044.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/waves/wave0045.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/waves/wave0046.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-01/waves/wave0047.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/COMPARISON.md`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/RECODING_TABLE.md`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/artifacts/deepseek-flash/fcl/carrier/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/artifacts/deepseek-flash/fcl/carrier/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/artifacts/deepseek-flash/fcl/carrier/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/artifacts/deepseek-flash/fcl/carrier/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/artifacts/deepseek-flash/fcl/carrier/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/artifacts/deepseek-flash/fcl/control/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/artifacts/deepseek-flash/fcl/control/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/artifacts/deepseek-flash/fcl/control/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/artifacts/deepseek-flash/fcl/control/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/artifacts/deepseek-flash/fcl/control/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/artifacts/deepseek-flash/fcl/original/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/artifacts/deepseek-flash/fcl/original/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/artifacts/deepseek-flash/fcl/original/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/artifacts/deepseek-flash/fcl/original/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/artifacts/deepseek-flash/fcl/original/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/artifacts/deepseek-flash/fcl/recoding/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/artifacts/deepseek-flash/fcl/recoding/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/artifacts/deepseek-flash/fcl/recoding/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/artifacts/deepseek-flash/fcl/recoding/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/artifacts/deepseek-flash/fcl/recoding/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/attempts/deepseek-flash/fcl/carrier/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/attempts/deepseek-flash/fcl/carrier/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/attempts/deepseek-flash/fcl/carrier/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/attempts/deepseek-flash/fcl/carrier/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/attempts/deepseek-flash/fcl/carrier/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/attempts/deepseek-flash/fcl/control/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/attempts/deepseek-flash/fcl/control/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/attempts/deepseek-flash/fcl/control/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/attempts/deepseek-flash/fcl/control/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/attempts/deepseek-flash/fcl/control/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/attempts/deepseek-flash/fcl/original/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/attempts/deepseek-flash/fcl/original/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/attempts/deepseek-flash/fcl/original/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/attempts/deepseek-flash/fcl/original/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/attempts/deepseek-flash/fcl/original/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/attempts/deepseek-flash/fcl/recoding/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/attempts/deepseek-flash/fcl/recoding/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/attempts/deepseek-flash/fcl/recoding/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/attempts/deepseek-flash/fcl/recoding/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/attempts/deepseek-flash/fcl/recoding/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/audit.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/briefs/fcl/carrier.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/briefs/fcl/control.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/briefs/fcl/original.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/briefs/fcl/recoding.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/briefs/prose/carrier.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/briefs/prose/control.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/briefs/prose/original.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/briefs/prose/recoding.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/comparison.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/juxtaposition/deepseek-flash__fcl.md`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/plan.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/preflight.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/provider/deepseek-flash/fcl/carrier/rep1/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/provider/deepseek-flash/fcl/carrier/rep1/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/provider/deepseek-flash/fcl/carrier/rep2/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/provider/deepseek-flash/fcl/carrier/rep2/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/provider/deepseek-flash/fcl/carrier/rep3/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/provider/deepseek-flash/fcl/carrier/rep3/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/provider/deepseek-flash/fcl/carrier/rep4/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/provider/deepseek-flash/fcl/carrier/rep4/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/provider/deepseek-flash/fcl/carrier/rep5/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/provider/deepseek-flash/fcl/carrier/rep5/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/provider/deepseek-flash/fcl/control/rep1/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/provider/deepseek-flash/fcl/control/rep1/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/provider/deepseek-flash/fcl/control/rep2/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/provider/deepseek-flash/fcl/control/rep2/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/provider/deepseek-flash/fcl/control/rep3/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/provider/deepseek-flash/fcl/control/rep3/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/provider/deepseek-flash/fcl/control/rep4/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/provider/deepseek-flash/fcl/control/rep4/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/provider/deepseek-flash/fcl/control/rep5/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/provider/deepseek-flash/fcl/control/rep5/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/provider/deepseek-flash/fcl/original/rep1/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/provider/deepseek-flash/fcl/original/rep1/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/provider/deepseek-flash/fcl/original/rep2/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/provider/deepseek-flash/fcl/original/rep2/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/provider/deepseek-flash/fcl/original/rep3/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/provider/deepseek-flash/fcl/original/rep3/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/provider/deepseek-flash/fcl/original/rep4/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/provider/deepseek-flash/fcl/original/rep4/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/provider/deepseek-flash/fcl/original/rep5/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/provider/deepseek-flash/fcl/original/rep5/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/provider/deepseek-flash/fcl/recoding/rep1/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/provider/deepseek-flash/fcl/recoding/rep1/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/provider/deepseek-flash/fcl/recoding/rep2/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/provider/deepseek-flash/fcl/recoding/rep2/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/provider/deepseek-flash/fcl/recoding/rep3/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/provider/deepseek-flash/fcl/recoding/rep3/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/provider/deepseek-flash/fcl/recoding/rep4/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/provider/deepseek-flash/fcl/recoding/rep4/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/provider/deepseek-flash/fcl/recoding/rep5/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/provider/deepseek-flash/fcl/recoding/rep5/call-0001.response.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/requests/deepseek-flash/fcl/carrier/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/requests/deepseek-flash/fcl/carrier/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/requests/deepseek-flash/fcl/carrier/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/requests/deepseek-flash/fcl/carrier/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/requests/deepseek-flash/fcl/carrier/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/requests/deepseek-flash/fcl/control/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/requests/deepseek-flash/fcl/control/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/requests/deepseek-flash/fcl/control/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/requests/deepseek-flash/fcl/control/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/requests/deepseek-flash/fcl/control/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/requests/deepseek-flash/fcl/original/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/requests/deepseek-flash/fcl/original/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/requests/deepseek-flash/fcl/original/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/requests/deepseek-flash/fcl/original/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/requests/deepseek-flash/fcl/original/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/requests/deepseek-flash/fcl/recoding/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/requests/deepseek-flash/fcl/recoding/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/requests/deepseek-flash/fcl/recoding/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/requests/deepseek-flash/fcl/recoding/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/requests/deepseek-flash/fcl/recoding/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/responses/deepseek-flash/fcl/carrier/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/responses/deepseek-flash/fcl/carrier/rep1.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/responses/deepseek-flash/fcl/carrier/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/responses/deepseek-flash/fcl/carrier/rep2.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/responses/deepseek-flash/fcl/carrier/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/responses/deepseek-flash/fcl/carrier/rep3.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/responses/deepseek-flash/fcl/carrier/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/responses/deepseek-flash/fcl/carrier/rep4.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/responses/deepseek-flash/fcl/carrier/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/responses/deepseek-flash/fcl/carrier/rep5.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/responses/deepseek-flash/fcl/control/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/responses/deepseek-flash/fcl/control/rep1.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/responses/deepseek-flash/fcl/control/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/responses/deepseek-flash/fcl/control/rep2.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/responses/deepseek-flash/fcl/control/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/responses/deepseek-flash/fcl/control/rep3.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/responses/deepseek-flash/fcl/control/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/responses/deepseek-flash/fcl/control/rep4.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/responses/deepseek-flash/fcl/control/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/responses/deepseek-flash/fcl/control/rep5.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/responses/deepseek-flash/fcl/original/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/responses/deepseek-flash/fcl/original/rep1.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/responses/deepseek-flash/fcl/original/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/responses/deepseek-flash/fcl/original/rep2.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/responses/deepseek-flash/fcl/original/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/responses/deepseek-flash/fcl/original/rep3.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/responses/deepseek-flash/fcl/original/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/responses/deepseek-flash/fcl/original/rep4.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/responses/deepseek-flash/fcl/original/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/responses/deepseek-flash/fcl/original/rep5.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/responses/deepseek-flash/fcl/recoding/rep1.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/responses/deepseek-flash/fcl/recoding/rep1.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/responses/deepseek-flash/fcl/recoding/rep2.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/responses/deepseek-flash/fcl/recoding/rep2.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/responses/deepseek-flash/fcl/recoding/rep3.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/responses/deepseek-flash/fcl/recoding/rep3.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/responses/deepseek-flash/fcl/recoding/rep4.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/responses/deepseek-flash/fcl/recoding/rep4.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/responses/deepseek-flash/fcl/recoding/rep5.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/responses/deepseek-flash/fcl/recoding/rep5.txt`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/waves/wave0001.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/waves/wave0002.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/waves/wave0003.json`
- `experiments/diagnostics/C001-contrast-triple/occurrence-02/waves/wave0004.json`
- `experiments/diagnostics/C001-contrast-triple/probe-2026-09-14/probe_ceiling.py`
- `experiments/diagnostics/C001-contrast-triple/probe-2026-09-14/records/deepseek-flash/ceiling-32768/call-0001.request.json`
- `experiments/diagnostics/C001-contrast-triple/probe-2026-09-14/records/deepseek-flash/ceiling-32768/call-0001.response.json`

### `experiments/diagnostics/F002-fork5-raised-clock` (108 files)

- `experiments/diagnostics/F002-fork5-raised-clock/PLAN.md`
- `experiments/diagnostics/F002-fork5-raised-clock/build/build_f002_material.py`
- `experiments/diagnostics/F002-fork5-raised-clock/build/build_runner_v3.py`
- `experiments/diagnostics/F002-fork5-raised-clock/material.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-01/artifacts/daily/mini_fcl/cycle01/account.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-01/artifacts/daily/mini_fcl/cycle01/objection.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-01/artifacts/daily/mini_fcl/cycle01/rival.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-01/attempts/daily/mini_fcl/cycle01/account.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-01/attempts/daily/mini_fcl/cycle01/objection.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-01/attempts/daily/mini_fcl/cycle01/response.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-01/attempts/daily/mini_fcl/cycle01/rival.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-01/plan.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-01/provider/daily/mini_fcl/cycle01/account/call-0001.request.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-01/provider/daily/mini_fcl/cycle01/account/call-0001.response.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-01/provider/daily/mini_fcl/cycle01/objection/call-0001.request.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-01/provider/daily/mini_fcl/cycle01/objection/call-0001.response.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-01/provider/daily/mini_fcl/cycle01/response/call-0001.request.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-01/provider/daily/mini_fcl/cycle01/response/call-0001.response.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-01/provider/daily/mini_fcl/cycle01/rival/call-0001.request.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-01/provider/daily/mini_fcl/cycle01/rival/call-0001.response.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-01/requests/daily/mini_fcl/cycle01/account.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-01/requests/daily/mini_fcl/cycle01/objection.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-01/requests/daily/mini_fcl/cycle01/response.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-01/requests/daily/mini_fcl/cycle01/rival.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-01/responses/daily/mini_fcl/cycle01/account.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-01/responses/daily/mini_fcl/cycle01/account.txt`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-01/responses/daily/mini_fcl/cycle01/objection.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-01/responses/daily/mini_fcl/cycle01/objection.txt`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-01/responses/daily/mini_fcl/cycle01/response.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-01/responses/daily/mini_fcl/cycle01/rival.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-01/responses/daily/mini_fcl/cycle01/rival.txt`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-01/traces/daily/mini_fcl/cycle01/account.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-01/traces/daily/mini_fcl/cycle01/objection.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-01/traces/daily/mini_fcl/cycle01/response.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-01/traces/daily/mini_fcl/cycle01/rival.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-01/waves/wave0001.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-01/waves/wave0002.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-01/waves/wave0003.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-02/artifacts/daily/mini_fcl/cycle01/account.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-02/artifacts/daily/mini_fcl/cycle01/carry.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-02/artifacts/daily/mini_fcl/cycle01/objection.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-02/artifacts/daily/mini_fcl/cycle01/response.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-02/artifacts/daily/mini_fcl/cycle01/rival.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-02/attempts/daily/mini_fcl/cycle01/account.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-02/attempts/daily/mini_fcl/cycle01/carry.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-02/attempts/daily/mini_fcl/cycle01/objection.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-02/attempts/daily/mini_fcl/cycle01/response.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-02/attempts/daily/mini_fcl/cycle01/rival.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-02/plan.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-02/provider/daily/mini_fcl/cycle01/account/call-0001.request.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-02/provider/daily/mini_fcl/cycle01/account/call-0001.response.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-02/provider/daily/mini_fcl/cycle01/carry/call-0001.request.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-02/provider/daily/mini_fcl/cycle01/carry/call-0001.response.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-02/provider/daily/mini_fcl/cycle01/objection/call-0001.request.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-02/provider/daily/mini_fcl/cycle01/objection/call-0001.response.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-02/provider/daily/mini_fcl/cycle01/response/call-0001.request.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-02/provider/daily/mini_fcl/cycle01/response/call-0001.response.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-02/provider/daily/mini_fcl/cycle01/rival/call-0001.request.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-02/provider/daily/mini_fcl/cycle01/rival/call-0001.response.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-02/requests/daily/mini_fcl/cycle01/account.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-02/requests/daily/mini_fcl/cycle01/carry.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-02/requests/daily/mini_fcl/cycle01/objection.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-02/requests/daily/mini_fcl/cycle01/response.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-02/requests/daily/mini_fcl/cycle01/rival.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-02/responses/daily/mini_fcl/cycle01/account.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-02/responses/daily/mini_fcl/cycle01/account.txt`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-02/responses/daily/mini_fcl/cycle01/carry.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-02/responses/daily/mini_fcl/cycle01/carry.txt`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-02/responses/daily/mini_fcl/cycle01/objection.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-02/responses/daily/mini_fcl/cycle01/objection.txt`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-02/responses/daily/mini_fcl/cycle01/response.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-02/responses/daily/mini_fcl/cycle01/response.txt`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-02/responses/daily/mini_fcl/cycle01/rival.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-02/responses/daily/mini_fcl/cycle01/rival.txt`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-02/traces/daily/mini_fcl/cycle01/account.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-02/traces/daily/mini_fcl/cycle01/carry.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-02/traces/daily/mini_fcl/cycle01/objection.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-02/traces/daily/mini_fcl/cycle01/response.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-02/traces/daily/mini_fcl/cycle01/rival.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-02/waves/wave0001.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-02/waves/wave0002.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-02/waves/wave0003.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-02/waves/wave0004.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-03/artifacts/daily/mini_fcl/cycle01/account.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-03/artifacts/daily/mini_fcl/cycle01/rival.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-03/attempts/daily/mini_fcl/cycle01/account.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-03/attempts/daily/mini_fcl/cycle01/objection.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-03/attempts/daily/mini_fcl/cycle01/rival.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-03/plan.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-03/provider/daily/mini_fcl/cycle01/account/call-0001.request.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-03/provider/daily/mini_fcl/cycle01/account/call-0001.response.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-03/provider/daily/mini_fcl/cycle01/objection/call-0001.request.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-03/provider/daily/mini_fcl/cycle01/objection/call-0001.response.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-03/provider/daily/mini_fcl/cycle01/rival/call-0001.request.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-03/provider/daily/mini_fcl/cycle01/rival/call-0001.response.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-03/requests/daily/mini_fcl/cycle01/account.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-03/requests/daily/mini_fcl/cycle01/objection.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-03/requests/daily/mini_fcl/cycle01/rival.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-03/responses/daily/mini_fcl/cycle01/account.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-03/responses/daily/mini_fcl/cycle01/account.txt`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-03/responses/daily/mini_fcl/cycle01/objection.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-03/responses/daily/mini_fcl/cycle01/rival.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-03/responses/daily/mini_fcl/cycle01/rival.txt`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-03/traces/daily/mini_fcl/cycle01/account.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-03/traces/daily/mini_fcl/cycle01/objection.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-03/traces/daily/mini_fcl/cycle01/rival.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-03/waves/wave0001.json`
- `experiments/diagnostics/F002-fork5-raised-clock/occurrence-03/waves/wave0002.json`

### `experiments/diagnostics/B001-bare-and-native` (2 files)

- `experiments/diagnostics/B001-bare-and-native/PLAN.md`
- `experiments/diagnostics/B001-bare-and-native/proposal-bare-deepseek.json`

A completeness claim is present: the use-table pages state *"Every byte this instrument read, with its sha256. Nothing under the occurrence was written."* and the B001 inventory carries a matching "Files read" table -- these claims bind the tables' own reads, not the whole directory, so unreferenced files above are informational only.

## Summary

Counts per verdict (each entry carries its manifest):

| verdict | total | per manifest |
|---|---|---|
| MATCH | 244 | experiments/diagnostics/C001-contrast-triple/material-occurrence-02.json: 8; experiments/diagnostics/C001-contrast-triple/material.json: 8; experiments/diagnostics/C001-contrast-triple/occurrence-01/material.json: 8; experiments/diagnostics/C001-contrast-triple/occurrence-01/preflight.json: 8; experiments/diagnostics/C001-contrast-triple/occurrence-02/material.json: 8; experiments/diagnostics/C001-contrast-triple/occurrence-02/preflight.json: 8; experiments/diagnostics/F002-fork5-raised-clock/material.json: 1; experiments/diagnostics/F002-fork5-raised-clock/occurrence-01/material.json: 1; experiments/diagnostics/F002-fork5-raised-clock/occurrence-02/material.json: 1; experiments/diagnostics/F002-fork5-raised-clock/occurrence-03/material.json: 1; experiments/diagnostics/H005-open-prose-commitments/material.json: 1; experiments/diagnostics/C001-contrast-triple/occurrence-01/plan.json: 9; experiments/diagnostics/C001-contrast-triple/occurrence-02/plan.json: 9; experiments/diagnostics/F002-fork5-raised-clock/occurrence-01/plan.json: 57; experiments/diagnostics/F002-fork5-raised-clock/occurrence-02/plan.json: 57; experiments/diagnostics/F002-fork5-raised-clock/occurrence-03/plan.json: 57; experiments/diagnostics/C001-contrast-triple/PLAN.md: 2 |
| MISMATCH | 0 | - |
| MISSING | 351 | experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json: 122; experiments/diagnostics/C001-contrast-triple/occurrence-01/plan.json: 1; experiments/diagnostics/C001-contrast-triple/occurrence-02/plan.json: 1; experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md: 122; experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-01/use-table/USE_TABLE.md: 32; experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/use-table/USE_TABLE.md: 49; experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-03/use-table/USE_TABLE.md: 23; experiments/diagnostics/C001-contrast-triple/PLAN.md: 1 |
| UNPARSED | 1 | src/creib/forge/mini/manifest.py: 1 |

### Every non-MATCH entry

| manifest | path | verdict | detail |
|---|---|---|---|
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-01/arms.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-01/artifacts/daily/bare/cycle01/answer.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-01/artifacts/daily/mini_fcl/cycle01/account.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-01/artifacts/daily/mini_fcl/cycle01/carry.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-01/artifacts/daily/mini_fcl/cycle01/objection.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-01/artifacts/daily/mini_fcl/cycle01/response.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-01/artifacts/daily/mini_fcl/cycle01/rival.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-01/artifacts/daily/mini_prose/cycle01/account.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-01/artifacts/daily/mini_prose/cycle01/carry.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-01/artifacts/daily/mini_prose/cycle01/objection.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-01/artifacts/daily/mini_prose/cycle01/response.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-01/artifacts/daily/mini_prose/cycle01/rival.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-01/artifacts/daily/native/cycle01/answer.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-01/plan.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-02/arms.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-02/artifacts/daily/bare/cycle01/answer.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-02/artifacts/daily/mini_fcl/cycle01/account.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-02/artifacts/daily/mini_fcl/cycle01/carry.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-02/artifacts/daily/mini_fcl/cycle01/objection.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-02/artifacts/daily/mini_fcl/cycle01/response.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-02/artifacts/daily/mini_fcl/cycle01/rival.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-02/artifacts/daily/mini_prose/cycle01/account.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-02/artifacts/daily/mini_prose/cycle01/carry.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-02/artifacts/daily/mini_prose/cycle01/objection.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-02/artifacts/daily/mini_prose/cycle01/response.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-02/artifacts/daily/mini_prose/cycle01/rival.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-02/plan.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-03/arms.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-03/artifacts/daily/bare/cycle01/answer.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-03/artifacts/daily/mini_fcl/cycle01/account.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-03/artifacts/daily/mini_fcl/cycle01/carry.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-03/artifacts/daily/mini_fcl/cycle01/objection.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-03/artifacts/daily/mini_fcl/cycle01/response.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-03/artifacts/daily/mini_fcl/cycle01/rival.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-03/artifacts/daily/mini_prose/cycle01/account.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-03/artifacts/daily/mini_prose/cycle01/carry.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-03/artifacts/daily/mini_prose/cycle01/objection.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-03/artifacts/daily/mini_prose/cycle01/response.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-03/artifacts/daily/mini_prose/cycle01/rival.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-03/plan.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-04/arms.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-04/artifacts/daily/bare/cycle01/answer.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-04/artifacts/daily/mini_fcl/cycle01/account.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-04/artifacts/daily/mini_prose/cycle01/account.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-04/artifacts/daily/mini_prose/cycle01/objection.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-04/artifacts/daily/mini_prose/cycle01/rival.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-04/plan.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-05/arms.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-05/artifacts/daily/bare/cycle01/answer.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-05/artifacts/daily/mini_fcl/cycle01/account.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-05/artifacts/daily/mini_fcl/cycle01/objection.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-05/artifacts/daily/mini_fcl/cycle01/rival.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-05/artifacts/daily/mini_prose/cycle01/account.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-05/artifacts/daily/mini_prose/cycle01/objection.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-05/artifacts/daily/mini_prose/cycle01/response.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-05/artifacts/daily/mini_prose/cycle01/rival.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-05/plan.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-06/arms.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-06/artifacts/daily/bare/cycle01/answer.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-06/artifacts/daily/mini_fcl/cycle01/account.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-06/artifacts/daily/mini_fcl/cycle01/carry.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-06/artifacts/daily/mini_fcl/cycle01/objection.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-06/artifacts/daily/mini_fcl/cycle01/response.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-06/artifacts/daily/mini_fcl/cycle01/rival.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-06/artifacts/daily/mini_prose/cycle01/account.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-06/artifacts/daily/mini_prose/cycle01/carry.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-06/artifacts/daily/mini_prose/cycle01/objection.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-06/artifacts/daily/mini_prose/cycle01/response.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-06/artifacts/daily/mini_prose/cycle01/rival.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-06/plan.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-07/arms.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-07/artifacts/daily/bare/cycle01/answer.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-07/artifacts/daily/mini_fcl/cycle01/account.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-07/artifacts/daily/mini_fcl/cycle01/rival.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-07/artifacts/daily/mini_prose/cycle01/account.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-07/artifacts/daily/mini_prose/cycle01/carry.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-07/artifacts/daily/mini_prose/cycle01/objection.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-07/artifacts/daily/mini_prose/cycle01/response.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-07/artifacts/daily/mini_prose/cycle01/rival.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-07/plan.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-08/arms.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-08/artifacts/daily/bare/cycle01/answer.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-08/artifacts/daily/mini_fcl/cycle01/account.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-08/artifacts/daily/mini_fcl/cycle01/objection.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-08/artifacts/daily/mini_fcl/cycle01/response.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-08/artifacts/daily/mini_fcl/cycle01/rival.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-08/artifacts/daily/mini_prose/cycle01/account.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-08/artifacts/daily/mini_prose/cycle01/carry.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-08/artifacts/daily/mini_prose/cycle01/objection.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-08/artifacts/daily/mini_prose/cycle01/response.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-08/artifacts/daily/mini_prose/cycle01/rival.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F001-fork5-multifamily/occurrence-08/plan.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F002-fork5-raised-clock/occurrence-01/arms.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F002-fork5-raised-clock/occurrence-01/artifacts/daily/mini_fcl/cycle01/account.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F002-fork5-raised-clock/occurrence-01/artifacts/daily/mini_fcl/cycle01/objection.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F002-fork5-raised-clock/occurrence-01/artifacts/daily/mini_fcl/cycle01/rival.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F002-fork5-raised-clock/occurrence-01/plan.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F002-fork5-raised-clock/occurrence-02/arms.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F002-fork5-raised-clock/occurrence-02/artifacts/daily/mini_fcl/cycle01/account.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F002-fork5-raised-clock/occurrence-02/artifacts/daily/mini_fcl/cycle01/carry.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F002-fork5-raised-clock/occurrence-02/artifacts/daily/mini_fcl/cycle01/objection.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F002-fork5-raised-clock/occurrence-02/artifacts/daily/mini_fcl/cycle01/response.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F002-fork5-raised-clock/occurrence-02/artifacts/daily/mini_fcl/cycle01/rival.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `F002-fork5-raised-clock/occurrence-02/plan.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `H005-open-prose-commitments/occurrence-01/artifacts/daily/bare/cycle01/answer.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `H005-open-prose-commitments/occurrence-01/artifacts/daily/matched/cycle01/account.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `H005-open-prose-commitments/occurrence-01/artifacts/daily/matched/cycle01/carry.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `H005-open-prose-commitments/occurrence-01/artifacts/daily/matched/cycle01/objection.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `H005-open-prose-commitments/occurrence-01/artifacts/daily/matched/cycle01/response.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `H005-open-prose-commitments/occurrence-01/artifacts/daily/matched/cycle01/rival.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_fcl/cycle01/account.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_fcl/cycle01/carry.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_fcl/cycle01/objection.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_fcl/cycle01/response.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_fcl/cycle01/rival.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_prose/cycle01/account.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_prose/cycle01/carry.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_prose/cycle01/objection.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_prose/cycle01/response.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_prose/cycle01/rival.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `H005-open-prose-commitments/occurrence-01/artifacts/daily/native/cycle01/answer.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/inventory.json` | `H005-open-prose-commitments/occurrence-01/plan.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/diagnostics/C001-contrast-triple/occurrence-01/plan.json` | `tools/contrast_triple_study.py` | MISSING | field helper_sha256; C001 PLAN.md names the driver as tools/contrast_triple_study.py (not copied into this sandbox) |
| `experiments/diagnostics/C001-contrast-triple/occurrence-02/plan.json` | `tools/contrast_triple_study.py` | MISSING | field helper_sha256; C001 PLAN.md names the driver as tools/contrast_triple_study.py (not copied into this sandbox) |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-01/arms.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-01/artifacts/daily/bare/cycle01/answer.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-01/artifacts/daily/mini_fcl/cycle01/account.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-01/artifacts/daily/mini_fcl/cycle01/carry.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-01/artifacts/daily/mini_fcl/cycle01/objection.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-01/artifacts/daily/mini_fcl/cycle01/response.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-01/artifacts/daily/mini_fcl/cycle01/rival.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-01/artifacts/daily/mini_prose/cycle01/account.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-01/artifacts/daily/mini_prose/cycle01/carry.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-01/artifacts/daily/mini_prose/cycle01/objection.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-01/artifacts/daily/mini_prose/cycle01/response.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-01/artifacts/daily/mini_prose/cycle01/rival.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-01/artifacts/daily/native/cycle01/answer.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-01/plan.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-02/arms.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-02/artifacts/daily/bare/cycle01/answer.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-02/artifacts/daily/mini_fcl/cycle01/account.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-02/artifacts/daily/mini_fcl/cycle01/carry.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-02/artifacts/daily/mini_fcl/cycle01/objection.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-02/artifacts/daily/mini_fcl/cycle01/response.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-02/artifacts/daily/mini_fcl/cycle01/rival.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-02/artifacts/daily/mini_prose/cycle01/account.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-02/artifacts/daily/mini_prose/cycle01/carry.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-02/artifacts/daily/mini_prose/cycle01/objection.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-02/artifacts/daily/mini_prose/cycle01/response.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-02/artifacts/daily/mini_prose/cycle01/rival.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-02/plan.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-03/arms.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-03/artifacts/daily/bare/cycle01/answer.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-03/artifacts/daily/mini_fcl/cycle01/account.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-03/artifacts/daily/mini_fcl/cycle01/carry.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-03/artifacts/daily/mini_fcl/cycle01/objection.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-03/artifacts/daily/mini_fcl/cycle01/response.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-03/artifacts/daily/mini_fcl/cycle01/rival.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-03/artifacts/daily/mini_prose/cycle01/account.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-03/artifacts/daily/mini_prose/cycle01/carry.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-03/artifacts/daily/mini_prose/cycle01/objection.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-03/artifacts/daily/mini_prose/cycle01/response.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-03/artifacts/daily/mini_prose/cycle01/rival.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-03/plan.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-04/arms.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-04/artifacts/daily/bare/cycle01/answer.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-04/artifacts/daily/mini_fcl/cycle01/account.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-04/artifacts/daily/mini_prose/cycle01/account.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-04/artifacts/daily/mini_prose/cycle01/objection.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-04/artifacts/daily/mini_prose/cycle01/rival.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-04/plan.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-05/arms.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-05/artifacts/daily/bare/cycle01/answer.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-05/artifacts/daily/mini_fcl/cycle01/account.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-05/artifacts/daily/mini_fcl/cycle01/objection.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-05/artifacts/daily/mini_fcl/cycle01/rival.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-05/artifacts/daily/mini_prose/cycle01/account.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-05/artifacts/daily/mini_prose/cycle01/objection.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-05/artifacts/daily/mini_prose/cycle01/response.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-05/artifacts/daily/mini_prose/cycle01/rival.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-05/plan.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-06/arms.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-06/artifacts/daily/bare/cycle01/answer.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-06/artifacts/daily/mini_fcl/cycle01/account.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-06/artifacts/daily/mini_fcl/cycle01/carry.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-06/artifacts/daily/mini_fcl/cycle01/objection.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-06/artifacts/daily/mini_fcl/cycle01/response.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-06/artifacts/daily/mini_fcl/cycle01/rival.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-06/artifacts/daily/mini_prose/cycle01/account.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-06/artifacts/daily/mini_prose/cycle01/carry.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-06/artifacts/daily/mini_prose/cycle01/objection.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-06/artifacts/daily/mini_prose/cycle01/response.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-06/artifacts/daily/mini_prose/cycle01/rival.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-06/plan.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-07/arms.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-07/artifacts/daily/bare/cycle01/answer.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-07/artifacts/daily/mini_fcl/cycle01/account.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-07/artifacts/daily/mini_fcl/cycle01/rival.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-07/artifacts/daily/mini_prose/cycle01/account.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-07/artifacts/daily/mini_prose/cycle01/carry.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-07/artifacts/daily/mini_prose/cycle01/objection.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-07/artifacts/daily/mini_prose/cycle01/response.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-07/artifacts/daily/mini_prose/cycle01/rival.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-07/plan.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-08/arms.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-08/artifacts/daily/bare/cycle01/answer.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-08/artifacts/daily/mini_fcl/cycle01/account.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-08/artifacts/daily/mini_fcl/cycle01/objection.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-08/artifacts/daily/mini_fcl/cycle01/response.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-08/artifacts/daily/mini_fcl/cycle01/rival.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-08/artifacts/daily/mini_prose/cycle01/account.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-08/artifacts/daily/mini_prose/cycle01/carry.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-08/artifacts/daily/mini_prose/cycle01/objection.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-08/artifacts/daily/mini_prose/cycle01/response.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-08/artifacts/daily/mini_prose/cycle01/rival.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F001-fork5-multifamily/occurrence-08/plan.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F002-fork5-raised-clock/occurrence-01/arms.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F002-fork5-raised-clock/occurrence-01/artifacts/daily/mini_fcl/cycle01/account.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F002-fork5-raised-clock/occurrence-01/artifacts/daily/mini_fcl/cycle01/objection.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F002-fork5-raised-clock/occurrence-01/artifacts/daily/mini_fcl/cycle01/rival.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F002-fork5-raised-clock/occurrence-01/plan.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F002-fork5-raised-clock/occurrence-02/arms.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F002-fork5-raised-clock/occurrence-02/artifacts/daily/mini_fcl/cycle01/account.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F002-fork5-raised-clock/occurrence-02/artifacts/daily/mini_fcl/cycle01/carry.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F002-fork5-raised-clock/occurrence-02/artifacts/daily/mini_fcl/cycle01/objection.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F002-fork5-raised-clock/occurrence-02/artifacts/daily/mini_fcl/cycle01/response.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F002-fork5-raised-clock/occurrence-02/artifacts/daily/mini_fcl/cycle01/rival.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `F002-fork5-raised-clock/occurrence-02/plan.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `H005-open-prose-commitments/occurrence-01/artifacts/daily/bare/cycle01/answer.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `H005-open-prose-commitments/occurrence-01/artifacts/daily/matched/cycle01/account.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `H005-open-prose-commitments/occurrence-01/artifacts/daily/matched/cycle01/carry.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `H005-open-prose-commitments/occurrence-01/artifacts/daily/matched/cycle01/objection.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `H005-open-prose-commitments/occurrence-01/artifacts/daily/matched/cycle01/response.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `H005-open-prose-commitments/occurrence-01/artifacts/daily/matched/cycle01/rival.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_fcl/cycle01/account.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_fcl/cycle01/carry.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_fcl/cycle01/objection.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_fcl/cycle01/response.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_fcl/cycle01/rival.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_prose/cycle01/account.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_prose/cycle01/carry.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_prose/cycle01/objection.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_prose/cycle01/response.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `H005-open-prose-commitments/occurrence-01/artifacts/daily/mini_prose/cycle01/rival.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `H005-open-prose-commitments/occurrence-01/artifacts/daily/native/cycle01/answer.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/B001-arm-inventory-2026-09-14/INVENTORY.md` | `H005-open-prose-commitments/occurrence-01/plan.json` | MISSING | referenced bytes live under experiments/diagnostics/F001-fork5-multifamily/, which was not copied into this sandbox |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-01/use-table/USE_TABLE.md` | `artifacts/daily/mini_fcl/cycle01/account.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-01/use-table/USE_TABLE.md` | `artifacts/daily/mini_fcl/cycle01/objection.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-01/use-table/USE_TABLE.md` | `artifacts/daily/mini_fcl/cycle01/rival.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-01/use-table/USE_TABLE.md` | `attempts/daily/mini_fcl/cycle01/account.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-01/use-table/USE_TABLE.md` | `attempts/daily/mini_fcl/cycle01/objection.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-01/use-table/USE_TABLE.md` | `attempts/daily/mini_fcl/cycle01/rival.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-01/use-table/USE_TABLE.md` | `manifests/fork5.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-01/use-table/USE_TABLE.md` | `manifests/return6.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-01/use-table/USE_TABLE.md` | `manifests/weave7.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-01/use-table/USE_TABLE.md` | `material.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-01/use-table/USE_TABLE.md` | `plan.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-01/use-table/USE_TABLE.md` | `provider/daily/mini_fcl/cycle01/account/call-0001.request.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-01/use-table/USE_TABLE.md` | `provider/daily/mini_fcl/cycle01/account/call-0001.response.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-01/use-table/USE_TABLE.md` | `provider/daily/mini_fcl/cycle01/objection/call-0001.request.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-01/use-table/USE_TABLE.md` | `provider/daily/mini_fcl/cycle01/objection/call-0001.response.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-01/use-table/USE_TABLE.md` | `provider/daily/mini_fcl/cycle01/rival/call-0001.request.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-01/use-table/USE_TABLE.md` | `provider/daily/mini_fcl/cycle01/rival/call-0001.response.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-01/use-table/USE_TABLE.md` | `requests/daily/mini_fcl/cycle01/account.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-01/use-table/USE_TABLE.md` | `requests/daily/mini_fcl/cycle01/objection.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-01/use-table/USE_TABLE.md` | `requests/daily/mini_fcl/cycle01/rival.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-01/use-table/USE_TABLE.md` | `responses/daily/mini_fcl/cycle01/account.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-01/use-table/USE_TABLE.md` | `responses/daily/mini_fcl/cycle01/account.txt` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-01/use-table/USE_TABLE.md` | `responses/daily/mini_fcl/cycle01/objection.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-01/use-table/USE_TABLE.md` | `responses/daily/mini_fcl/cycle01/objection.txt` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-01/use-table/USE_TABLE.md` | `responses/daily/mini_fcl/cycle01/rival.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-01/use-table/USE_TABLE.md` | `responses/daily/mini_fcl/cycle01/rival.txt` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-01/use-table/USE_TABLE.md` | `traces/daily/mini_fcl/cycle01/account.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-01/use-table/USE_TABLE.md` | `traces/daily/mini_fcl/cycle01/objection.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-01/use-table/USE_TABLE.md` | `traces/daily/mini_fcl/cycle01/rival.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-01/use-table/USE_TABLE.md` | `waves/wave0001.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-01/use-table/USE_TABLE.md` | `waves/wave0002.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-01/use-table/USE_TABLE.md` | `waves/wave0003.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/use-table/USE_TABLE.md` | `artifacts/daily/mini_fcl/cycle01/account.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/use-table/USE_TABLE.md` | `artifacts/daily/mini_fcl/cycle01/carry.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/use-table/USE_TABLE.md` | `artifacts/daily/mini_fcl/cycle01/objection.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/use-table/USE_TABLE.md` | `artifacts/daily/mini_fcl/cycle01/response.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/use-table/USE_TABLE.md` | `artifacts/daily/mini_fcl/cycle01/rival.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/use-table/USE_TABLE.md` | `attempts/daily/mini_fcl/cycle01/account.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/use-table/USE_TABLE.md` | `attempts/daily/mini_fcl/cycle01/carry.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/use-table/USE_TABLE.md` | `attempts/daily/mini_fcl/cycle01/objection.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/use-table/USE_TABLE.md` | `attempts/daily/mini_fcl/cycle01/response.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/use-table/USE_TABLE.md` | `attempts/daily/mini_fcl/cycle01/rival.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/use-table/USE_TABLE.md` | `manifests/fork5.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/use-table/USE_TABLE.md` | `manifests/return6.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/use-table/USE_TABLE.md` | `manifests/weave7.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/use-table/USE_TABLE.md` | `material.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/use-table/USE_TABLE.md` | `plan.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/use-table/USE_TABLE.md` | `provider/daily/mini_fcl/cycle01/account/call-0001.request.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/use-table/USE_TABLE.md` | `provider/daily/mini_fcl/cycle01/account/call-0001.response.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/use-table/USE_TABLE.md` | `provider/daily/mini_fcl/cycle01/carry/call-0001.request.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/use-table/USE_TABLE.md` | `provider/daily/mini_fcl/cycle01/carry/call-0001.response.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/use-table/USE_TABLE.md` | `provider/daily/mini_fcl/cycle01/objection/call-0001.request.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/use-table/USE_TABLE.md` | `provider/daily/mini_fcl/cycle01/objection/call-0001.response.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/use-table/USE_TABLE.md` | `provider/daily/mini_fcl/cycle01/response/call-0001.request.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/use-table/USE_TABLE.md` | `provider/daily/mini_fcl/cycle01/response/call-0001.response.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/use-table/USE_TABLE.md` | `provider/daily/mini_fcl/cycle01/rival/call-0001.request.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/use-table/USE_TABLE.md` | `provider/daily/mini_fcl/cycle01/rival/call-0001.response.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/use-table/USE_TABLE.md` | `requests/daily/mini_fcl/cycle01/account.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/use-table/USE_TABLE.md` | `requests/daily/mini_fcl/cycle01/carry.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/use-table/USE_TABLE.md` | `requests/daily/mini_fcl/cycle01/objection.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/use-table/USE_TABLE.md` | `requests/daily/mini_fcl/cycle01/response.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/use-table/USE_TABLE.md` | `requests/daily/mini_fcl/cycle01/rival.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/use-table/USE_TABLE.md` | `responses/daily/mini_fcl/cycle01/account.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/use-table/USE_TABLE.md` | `responses/daily/mini_fcl/cycle01/account.txt` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/use-table/USE_TABLE.md` | `responses/daily/mini_fcl/cycle01/carry.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/use-table/USE_TABLE.md` | `responses/daily/mini_fcl/cycle01/carry.txt` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/use-table/USE_TABLE.md` | `responses/daily/mini_fcl/cycle01/objection.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/use-table/USE_TABLE.md` | `responses/daily/mini_fcl/cycle01/objection.txt` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/use-table/USE_TABLE.md` | `responses/daily/mini_fcl/cycle01/response.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/use-table/USE_TABLE.md` | `responses/daily/mini_fcl/cycle01/response.txt` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/use-table/USE_TABLE.md` | `responses/daily/mini_fcl/cycle01/rival.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/use-table/USE_TABLE.md` | `responses/daily/mini_fcl/cycle01/rival.txt` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/use-table/USE_TABLE.md` | `traces/daily/mini_fcl/cycle01/account.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/use-table/USE_TABLE.md` | `traces/daily/mini_fcl/cycle01/carry.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/use-table/USE_TABLE.md` | `traces/daily/mini_fcl/cycle01/objection.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/use-table/USE_TABLE.md` | `traces/daily/mini_fcl/cycle01/response.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/use-table/USE_TABLE.md` | `traces/daily/mini_fcl/cycle01/rival.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/use-table/USE_TABLE.md` | `waves/wave0001.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/use-table/USE_TABLE.md` | `waves/wave0002.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/use-table/USE_TABLE.md` | `waves/wave0003.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-02/use-table/USE_TABLE.md` | `waves/wave0004.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-03/use-table/USE_TABLE.md` | `artifacts/daily/mini_fcl/cycle01/account.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-03/use-table/USE_TABLE.md` | `artifacts/daily/mini_fcl/cycle01/rival.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-03/use-table/USE_TABLE.md` | `attempts/daily/mini_fcl/cycle01/account.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-03/use-table/USE_TABLE.md` | `attempts/daily/mini_fcl/cycle01/rival.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-03/use-table/USE_TABLE.md` | `manifests/fork5.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-03/use-table/USE_TABLE.md` | `manifests/return6.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-03/use-table/USE_TABLE.md` | `manifests/weave7.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-03/use-table/USE_TABLE.md` | `material.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-03/use-table/USE_TABLE.md` | `plan.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-03/use-table/USE_TABLE.md` | `provider/daily/mini_fcl/cycle01/account/call-0001.request.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-03/use-table/USE_TABLE.md` | `provider/daily/mini_fcl/cycle01/account/call-0001.response.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-03/use-table/USE_TABLE.md` | `provider/daily/mini_fcl/cycle01/rival/call-0001.request.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-03/use-table/USE_TABLE.md` | `provider/daily/mini_fcl/cycle01/rival/call-0001.response.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-03/use-table/USE_TABLE.md` | `requests/daily/mini_fcl/cycle01/account.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-03/use-table/USE_TABLE.md` | `requests/daily/mini_fcl/cycle01/rival.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-03/use-table/USE_TABLE.md` | `responses/daily/mini_fcl/cycle01/account.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-03/use-table/USE_TABLE.md` | `responses/daily/mini_fcl/cycle01/account.txt` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-03/use-table/USE_TABLE.md` | `responses/daily/mini_fcl/cycle01/rival.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-03/use-table/USE_TABLE.md` | `responses/daily/mini_fcl/cycle01/rival.txt` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-03/use-table/USE_TABLE.md` | `traces/daily/mini_fcl/cycle01/account.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-03/use-table/USE_TABLE.md` | `traces/daily/mini_fcl/cycle01/rival.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-03/use-table/USE_TABLE.md` | `waves/wave0001.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/analyses/F002-fork5-raised-clock-2026-09-14/occurrence-03/use-table/USE_TABLE.md` | `waves/wave0002.json` | MISSING | referenced bytes live under the occurrence trees of experiments/diagnostics/F002-fork5-raised-clock (or F001), not under this analyses directory |
| `experiments/diagnostics/C001-contrast-triple/PLAN.md` | `plan_id` | MISSING | pinned bytes not copied into this sandbox |
| `src/creib/forge/mini/manifest.py` | `src/creib/forge/mini/manifest.py` | UNPARSED | filename matches the manifest rule but the content is not a path->digest list (it is source code / a template-schema JSON; F002 manifests/*.json are pinned by plan.json.manifests) |

### Credential scan

Patterns `sk-[0-9a-f]{32}` and `[0-9a-f]{32}\.[A-Za-z0-9_-]{20,}` over every walked file: **0 hits** (expected zero).

### Blind spots of this walk

- It sees only files that were copied into this sandbox; a MISSING verdict means "the pinned bytes are not in this copy", not that the digest in the manifest is wrong.
- Digests keyed by something other than a file path (node coordinates, spec ids, `record_sha256`/`provider_*_sha256` fields, `helper_sha256` of absent drivers) are reported but cannot be cross-checked against their canonical object by hashing a path.
- Nested (non top-level) path-to-digest maps under other key names than the scanned set, and digest lists inside prose without the ``| `path` | `sha256` |`` shape, are not found.
- plan_id itself ("digest of the frozen plan body") was not re-derived: the files state it is a digest but do not state the canonical-JSON rule in a way this script implements.
