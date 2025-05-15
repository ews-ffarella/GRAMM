.PHONY: build
build:
	dotnet build src --configuration Release

.PHONY: publish
publish: clean
	dotnet publish src --runtime win-x64 --configuration Release -p:PublishSingleFile=true -p:PublishTrimmed=true
	cp -f ./src/bin/Release/net8.0/win-x64/publish/EWS_GRAMM.exe ../ValidationCases/Bin

.PHONY: publish_linux
publish_linux:
	dotnet publish src --runtime linux-x64 --configuration Release -p:PublishSingleFile=true -p:PublishTrimmed=true
	sudo cp ./src/bin/Release/net8.0/linux-x64/publish/EWS_GRAMM /usr/local/bin
	sudo chmod a+x /usr/local/bin/EWS_GRAMM

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
test_a_coarse: 
	dotnet run --project ./src "../ValidationCases/Askervein_coarse" 1 1

.PHONY: test_a_fine
test_a_fine: publish
	./src/bin/Release/net8.0/win10-x64/publish/EWS_GRAMM.exe "./ValidationCases/Askervein_fine" 1 7
	#dotnet run --project ./src "./test/Askervein_fine" 1 1

.PHONY: test_gui
test_gui: publish
	dotnet run --project ./src "../ValidationCases/hwr" 1 1