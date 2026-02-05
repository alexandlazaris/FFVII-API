# CHANGELOG


## v2.2.0 (2026-02-05)

### Continuous Integration

- Modify secret name
  ([`c0d4f36`](https://github.com/alexandlazaris/FFVII-API/commit/c0d4f363a595ad894d6bda48deee63f08bcf98ba))

- Modify secret name used in workflow
  ([`ef5e3b8`](https://github.com/alexandlazaris/FFVII-API/commit/ef5e3b8e490a0896e4c8b6ed18693a1a6a8accf2))

### Features

- Add cors support
  ([`899d013`](https://github.com/alexandlazaris/FFVII-API/commit/899d013185aa01a9371c265601a407fa6c047045))


## v2.1.2 (2025-11-05)

### Bug Fixes

- Increase element length to 20
  ([`8cc18b3`](https://github.com/alexandlazaris/FFVII-API/commit/8cc18b37ec58dcc7b1665d67c42920cc36c8a92c))


## v2.1.1 (2025-11-04)

### Bug Fixes

- Apply the correct column change syntax for element length
  ([`8d67ad2`](https://github.com/alexandlazaris/FFVII-API/commit/8d67ad29d237b906919ff9f0f6dde864819eb6c0))

### Continuous Integration

- Remove unused env var
  ([`a09d37c`](https://github.com/alexandlazaris/FFVII-API/commit/a09d37caa8383f5f022071967765b9c8fb04d087))


## v2.1.0 (2025-11-04)

### Bug Fixes

- Remove unused import
  ([`f2d31d8`](https://github.com/alexandlazaris/FFVII-API/commit/f2d31d8897942488bc5eda444b1f8e5074ebff01))

- Resolve type differences for seed data
  ([`97f1254`](https://github.com/alexandlazaris/FFVII-API/commit/97f1254019584de148932250eca0de2c1c9a549a))

- Upgrade flask patch version to resolve dependabot issue #1
  ([`7a5cd62`](https://github.com/alexandlazaris/FFVII-API/commit/7a5cd62c6bcc1e171a94c6e2adef3a88ebad4fd0))

### Chores

- Fix formatting in migration file
  ([`c24927a`](https://github.com/alexandlazaris/FFVII-API/commit/c24927a009b3836d395ea77da31ccf6536449ae6))

- Remove unneeded migration command
  ([`943bc49`](https://github.com/alexandlazaris/FFVII-API/commit/943bc49d099dc3f891466637a7eddade0ee87e87))

### Continuous Integration

- Include badge generation commands
  ([`020b20b`](https://github.com/alexandlazaris/FFVII-API/commit/020b20b25d7de06e83142bfecb3772122aaa0ddc))

### Documentation

- Custom badges directory
  ([`7f6dfe9`](https://github.com/alexandlazaris/FFVII-API/commit/7f6dfe93890508e72074c185e00ea7a641317d4d))

- Include custom badge generation
  ([`327472d`](https://github.com/alexandlazaris/FFVII-API/commit/327472d31981fdf80376de747e5d82344b04f021))

### Features

- Add filtering to GET /materia + limit the POST data
  ([`3d9f4ac`](https://github.com/alexandlazaris/FFVII-API/commit/3d9f4ac9403ac95063eca95d0aab67a24a2a9678))

- Moved api logic for materia into separate service module & removed unused api route + matching
  test
  ([`8521d10`](https://github.com/alexandlazaris/FFVII-API/commit/8521d10c835f8610dd7adf2d276dbe8ae4019b44))

- Query params schema for GET /materia
  ([`ba10ee8`](https://github.com/alexandlazaris/FFVII-API/commit/ba10ee832c30a820c772470bc8eac79f27359510))

- Seed full materia data into db, updated model & add migration
  ([`35cee1a`](https://github.com/alexandlazaris/FFVII-API/commit/35cee1ad66c483ea812a9ec34a0dbd2e3dfca550))

- Sort name by asc/desc
  ([`f14183c`](https://github.com/alexandlazaris/FFVII-API/commit/f14183c203203f2fb200c8d263fa9a9662ffbf96))

### Testing

- Add new unit tests for asc/desc sort
  ([`6c657d3`](https://github.com/alexandlazaris/FFVII-API/commit/6c657d3b4b4e7c65f37d8c2cf69379c30015559c))

- Add test for DELETE /materia
  ([`8f23400`](https://github.com/alexandlazaris/FFVII-API/commit/8f234002c34f620fe150db3eb0adbe9b333de8a9))

- Manually seed data into db for 1 test & add extra assertions
  ([`624bace`](https://github.com/alexandlazaris/FFVII-API/commit/624bace50de2720c236a50bd0c9de64d8f26968e))


## v2.0.2 (2025-10-30)

### Bug Fixes

- Change default disc to 1
  ([`a4f0141`](https://github.com/alexandlazaris/FFVII-API/commit/a4f01413a729f1f949f49f6d2215dd9784136861))


## v2.0.1 (2025-10-01)

### Bug Fixes

- Correct the flask db commands
  ([`3b6acc8`](https://github.com/alexandlazaris/FFVII-API/commit/3b6acc8f61ab75fdc3544289eeb6e007418eebac))

- Remove unneeded line
  ([`f411d19`](https://github.com/alexandlazaris/FFVII-API/commit/f411d196bb7f72ccb8620f49652db69344c942dc))

- Replace depricated orm function with new feature to get records
  ([`cb2f6f4`](https://github.com/alexandlazaris/FFVII-API/commit/cb2f6f484b7263e610a1bbf7b386d44ffaa81ddd))

- Split up db url setting
  ([`453462c`](https://github.com/alexandlazaris/FFVII-API/commit/453462c6875b343189c809288cffefa449d92708))

- Update failing unit test logic
  ([`43f8982`](https://github.com/alexandlazaris/FFVII-API/commit/43f89820e77fa58d5a77daf615348d42d8000987))

### Chores

- Added temp mdoel change to trigger db migration
  ([`cbce42f`](https://github.com/alexandlazaris/FFVII-API/commit/cbce42f1451d8cb8cbce848fb6757767bf3eec2d))

### Continuous Integration

- Change false check
  ([`bc765fa`](https://github.com/alexandlazaris/FFVII-API/commit/bc765fa9649486775a1c5e4ebddf72054432e80f))

- Change manual trigger workflow
  ([`5a66cdc`](https://github.com/alexandlazaris/FFVII-API/commit/5a66cdc834b43615fa844e48eeca68ed2b362443))

- Change text input to choice list
  ([`bc5965f`](https://github.com/alexandlazaris/FFVII-API/commit/bc5965fb2fa162fdf10ebba1431df8349fc061ad))

- Change type to boolean
  ([`ab8f9a5`](https://github.com/alexandlazaris/FFVII-API/commit/ab8f9a5851a1c49ec16c0b211c622a35b3cebb81))

- Fix default value for existing saves
  ([`982c429`](https://github.com/alexandlazaris/FFVII-API/commit/982c42985acbc535e6308ec65960574091b22af4))

- Fix step syntax
  ([`6b628f3`](https://github.com/alexandlazaris/FFVII-API/commit/6b628f306d8989bb9307df1360c1bcb48c68dd34))

- Logging
  ([`b2cac99`](https://github.com/alexandlazaris/FFVII-API/commit/b2cac9950533e6efedc78222bc7aca5342a8c4c7))

- Manual workflow trigger ([#15](https://github.com/alexandlazaris/FFVII-API/pull/15),
  [`b23d000`](https://github.com/alexandlazaris/FFVII-API/commit/b23d000bf3b2995eccd85c5880d5bf274a16fa69))

- Remove 'environment' from unit tests workflow
  ([`d93da04`](https://github.com/alexandlazaris/FFVII-API/commit/d93da0435648698342c09b596d69ec180078c119))

- Remove feat branch from workflow
  ([`2cfb36c`](https://github.com/alexandlazaris/FFVII-API/commit/2cfb36c8ddc06829170d5b5c05878ed0911588fb))

- Remove unnecessary html output
  ([`2e3f011`](https://github.com/alexandlazaris/FFVII-API/commit/2e3f011839dc84f93571347b71c754c6ae797c1e))

- Restore default coverage trigger
  ([`05e3e2c`](https://github.com/alexandlazaris/FFVII-API/commit/05e3e2c96741530705e7c05928d0c4701316e6a9))

- Restore original token
  ([`9cbc14d`](https://github.com/alexandlazaris/FFVII-API/commit/9cbc14d2cea1646f75f903b388f7e12ba2588bb0))

- Run unit tests only on feature branch push
  ([`7162c0f`](https://github.com/alexandlazaris/FFVII-API/commit/7162c0fffbad884c736fcc5ad7c6ae9802191201))

- Run unit tests with pytest
  ([`f7466ec`](https://github.com/alexandlazaris/FFVII-API/commit/f7466ece36b7bab66561d3a785c7d5f93aaa0a96))

- Syntax on input
  ([`fdb36bc`](https://github.com/alexandlazaris/FFVII-API/commit/fdb36bc67be656869450c95286867ce9aafcaf08))

- Temp logging added to see failure in ci
  ([`9f7ae5d`](https://github.com/alexandlazaris/FFVII-API/commit/9f7ae5db7996d1a8088bc1cbcd4539c46b3aeca8))

- Trigger local db migration before running tests
  ([`d084729`](https://github.com/alexandlazaris/FFVII-API/commit/d084729e19c2c66eb6c2c0ddf84079fb3feabaf7))

- Try out new token
  ([`6a8230e`](https://github.com/alexandlazaris/FFVII-API/commit/6a8230e68c51bc418004ed37f1e2b2eadd51f31b))

- Unit test workflow + minor tweaks to manual trigger
  ([`ff0ec69`](https://github.com/alexandlazaris/FFVII-API/commit/ff0ec697c15b9aa5852f2fabf23e8a311e3e8f6f))

- Wording of quit msg
  ([`1acff5e`](https://github.com/alexandlazaris/FFVII-API/commit/1acff5e762898bb34684a02ec2bec28e266d15f2))

### Documentation

- Add readme code snippet of /saves response
  ([`2a3e059`](https://github.com/alexandlazaris/FFVII-API/commit/2a3e059939cb5d33f23d5ff1db51d0ea03095f2e))

- Add release badge
  ([`6bdead2`](https://github.com/alexandlazaris/FFVII-API/commit/6bdead2bf7bdc443dc66371faf735e500fcf6bd4))

- Add unit test badge
  ([`545d997`](https://github.com/alexandlazaris/FFVII-API/commit/545d9978d767d1e6536129b462b8bc7dad701f67))


## v2.0.0 (2025-07-08)

### Features

- Dummy change to force a major version bump
  ([`53021e3`](https://github.com/alexandlazaris/FFVII-API/commit/53021e319ebcdecbe7fc104453ed1edef5dcd406))

BREAKING CHANGE: This is an intentional breaking change to force a major version.

### Breaking Changes

- This is an intentional breaking change to force a major version.


## v1.4.0 (2025-07-08)

### Chores

- Removed unused print
  ([`7c55e3b`](https://github.com/alexandlazaris/FFVII-API/commit/7c55e3bdd2956a961240a159f7a7a3159c880820))

### Code Style

- Removed print logs
  ([`99a3f7e`](https://github.com/alexandlazaris/FFVII-API/commit/99a3f7e8c7294524c9151642eb74195f7f06bc2d))

### Continuous Integration

- Edit container ports
  ([`43adcb1`](https://github.com/alexandlazaris/FFVII-API/commit/43adcb18ab164481b56ba44b20c8a8e66957b410))

### Documentation

- Added unit test tip
  ([`84123cb`](https://github.com/alexandlazaris/FFVII-API/commit/84123cbde86f7fccec6ee868949d0046d37b0446))

- Cleaned up readme of bloat, add local run guide & API feature highlights
  ([`b5696bf`](https://github.com/alexandlazaris/FFVII-API/commit/b5696bfe3b7fefa93d32ae88bf3b76537b72b800))

- Create LICENSE
  ([`5870691`](https://github.com/alexandlazaris/FFVII-API/commit/5870691ad6bd1544a8dd48833e13c74fd69be753))

- Update features list
  ([`da6853c`](https://github.com/alexandlazaris/FFVII-API/commit/da6853cc12662dc76c9ba44621a3f4037e4c37ac))

- Updated run steps
  ([`bb18b3d`](https://github.com/alexandlazaris/FFVII-API/commit/bb18b3d89007a12c4a50192a157ff3b5c71a9416))

### Features

- Added service to handle party routes
  ([`1fe1328`](https://github.com/alexandlazaris/FFVII-API/commit/1fe13287c898e8569c8a3d4e15e6c13b2f44e8f3))

- Cleaned up save service, added rollbacks
  ([`39839e7`](https://github.com/alexandlazaris/FFVII-API/commit/39839e77bbd419532f8ac34ac18a1e01a44c05bd))

- Customise party objects when getting saves
  ([`1d269e0`](https://github.com/alexandlazaris/FFVII-API/commit/1d269e05b00456aa69a6969c1bc642451c6dcf8f))

- Get single party member schema
  ([`738c010`](https://github.com/alexandlazaris/FFVII-API/commit/738c010ca43883d10c108f1c7907354b21f3b515))

- Import new Saves route
  ([`a64fdf8`](https://github.com/alexandlazaris/FFVII-API/commit/a64fdf8c3dcec1b24176daa32bad9999a046a95d))

- Improve schema independence for party routes
  ([`eed55aa`](https://github.com/alexandlazaris/FFVII-API/commit/eed55aa67f29f236a29bc438ed36bcac789d4949))

- Improve schema independence for save routes
  ([`9a37fc9`](https://github.com/alexandlazaris/FFVII-API/commit/9a37fc949575ae3637cf3d8e0bf4cb970073e5fb))

- Refactor how to add parties & validations involved
  ([`5aa26b5`](https://github.com/alexandlazaris/FFVII-API/commit/5aa26b5f0e75a6222edbb56c9e648f2a53a3d7b3))

- Saves now return party members
  ([`e5f1f49`](https://github.com/alexandlazaris/FFVII-API/commit/e5f1f49353f48ce70154b8fda31dd4bbddd6577f))


## v1.3.1 (2025-04-19)

### Bug Fixes

- Run migration to restore tables
  ([`e599d88`](https://github.com/alexandlazaris/FFVII-API/commit/e599d88938ec9aa80dcb8c308d8d510af3f9d5a7))

- Use correct status code
  ([`9486c5b`](https://github.com/alexandlazaris/FFVII-API/commit/9486c5b36e78d81e2b3fde87aecf04cc3b24f443))

### Chores

- Ignore warnings & unit test outputs
  ([`302fd9c`](https://github.com/alexandlazaris/FFVII-API/commit/302fd9c80a8493160ae09737b4054c14a232f931))

- Replace outdated code from warning
  ([`f465279`](https://github.com/alexandlazaris/FFVII-API/commit/f4652799a0f0fa772fe46b93a76b55b5922c731b))

### Documentation

- Add todo item + unit test guide
  ([`77e1762`](https://github.com/alexandlazaris/FFVII-API/commit/77e1762a1943ec8f41913b93d0f5c0c80d65c586))

### Testing

- Add unit test beginnings, catch exception when fetching characters fails
  ([`18a0a88`](https://github.com/alexandlazaris/FFVII-API/commit/18a0a88963f5047376d3e80afc16b50115924d77))

- More unit tests
  ([`b6cdc31`](https://github.com/alexandlazaris/FFVII-API/commit/b6cdc31da0f3757fc05c8ea1259dc417eb1f77cc))


## v1.3.0 (2025-04-16)

### Continuous Integration

- Add tools prefix to root table
  ([`47b3c64`](https://github.com/alexandlazaris/FFVII-API/commit/47b3c64d9fab65c22f98259e4fd49369d750c799))

- Add verbose logging
  ([`7319c5c`](https://github.com/alexandlazaris/FFVII-API/commit/7319c5c7111763e2d9d7bc33f564bff234805e79))

- Added semantic release workflow
  ([`8e492fd`](https://github.com/alexandlazaris/FFVII-API/commit/8e492fdd04f2c04568eadde84965b7e39dca0d90))

- Correcting the repo_dir path
  ([`3e7e993`](https://github.com/alexandlazaris/FFVII-API/commit/3e7e993407b73feae788c032a35eb93f63d32b7b))

- Delete CHANGELOG.md
  ([`7940ad0`](https://github.com/alexandlazaris/FFVII-API/commit/7940ad0a42a555989237c3cdf8762130a0e505a7))

- Removed changelog.changelog_file
  ([`6e1e3d9`](https://github.com/alexandlazaris/FFVII-API/commit/6e1e3d931a8d53a8e53ebb86421237929147cfed))

- Revert changes to release branches
  ([`d9f3b88`](https://github.com/alexandlazaris/FFVII-API/commit/d9f3b88af26f741ad06f4551231fe1043516645b))

- Run actions on temp branch
  ([`8bfa1ef`](https://github.com/alexandlazaris/FFVII-API/commit/8bfa1ef747339b2672667cba96f10278ac0b1fc1))

### Documentation

- Completed todo item
  ([`c7965db`](https://github.com/alexandlazaris/FFVII-API/commit/c7965dbebc24703fccc1089eaa2f2f6484818154))

### Features

- Force feat commit
  ([`32b25d7`](https://github.com/alexandlazaris/FFVII-API/commit/32b25d788879e38f8634cda05249c15f0f6e40ed))


## v1.2.0 (2025-04-15)


## v1.1.0 (2025-04-07)
