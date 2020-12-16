.PHONY: build
build:
	dotnet build src --configuration Release

.PHONY: publish
publish: clean
	dotnet publish src -r win10-x64 -c Release -p:PublishSingleFile=true -p:PublishTrimmed=true
	cp -f ./src/bin/Release/netcoreapp3.1/win10-x64/publish/GRAMM.exe ../ValidationCases/Bin

.PHONY: publish_linux
publish_linux:
	dotnet publish src -r linux-x64 -c Release -p:PublishSingleFile=true -p:PublishTrimmed=true

.PHONY: clean
clean:
	dotnet clean src
	rm -rf ./src/bin | true
	rm -rf ./src/obj | true

.PHONY: test_clean
test_clean:
	find test -name "*.*wnd" -type f | xargs rm -f
	find test -name "*.probes.dat" -type f | xargs rm -f
	find test -name "*.scl" -type f | xargs rm -f
	find test -name "*_steady_state.txt" -type f | xargs rm -f
	find test -name "albeq.dat" -type f | xargs rm -f
	find test -name "Logfile_GRAMMCore.txt" -type f | xargs rm -f
	find test -name "PercentGramm.txt" -type f | xargs rm -f
	

.PHONY: test_a_coarse
test_a_coarse: publish
	./src/bin/Release/netcoreapp3.1/win10-x64/publish/GRAMM.exe "./test/Askervein_coarse" 1 7

.PHONY: test_a_fine
test_a_fine: publish
	./src/bin/Release/netcoreapp3.1/win10-x64/publish/GRAMM.exe "./test/Askervein_fine" 1 7
	#dotnet run --project ./src "./test/Askervein_fine" 1 1