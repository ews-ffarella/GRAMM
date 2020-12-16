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
	rm -rf ./src/bin
	rm -rf ./src/obj

.PHONY: test_a_coarse
test_a_coarse: publish
	./src/bin/Release/netcoreapp3.1/win10-x64/publish/GRAMM.exe "./test/Askervein_coarse" 1 7

.PHONY: test_a_fine
test_a_fine: publish
	./src/bin/Release/netcoreapp3.1/win10-x64/publish/GRAMM.exe "./test/Askervein_fine" 1 7
	#dotnet run --project ./src "./test/Askervein_fine" 1 1