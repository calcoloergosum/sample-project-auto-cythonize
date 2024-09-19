import package
import package.a
import package.b.b

def test_functions():
    print(package.__path__)
    assert package.a.a() == 'a'
    assert package.b.b.b() == 'b'
    assert package.SOME_MODULE_ATTRIBUTE == 'some value'
    assert package.b.SOME_MODULE_ATTRIBUTE == 42
