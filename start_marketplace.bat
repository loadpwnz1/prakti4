python -m pip install -r marketplace/requirements.txt
cmd /c venv\Scripts\activate.bat
cd marketplace
python -m grpc_tools.protoc -I ../protobufs --python_out=. --grpc_python_out=. ../protobufs/recommendations.proto
python marketplace.py
pause