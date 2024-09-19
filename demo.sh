# Any version of python of your choice
python3.10 -m venv env
source env/bin/activate

pip install build
rm -r dist > /dev/null 2>&1
python -m build --wheel

cd tests
pip uninstall -y pyproject-cython-test
pip install --force-reinstall ../dist/*.whl

pip install pytest
which pytest
pytest test_functions.py -s
cd ..
