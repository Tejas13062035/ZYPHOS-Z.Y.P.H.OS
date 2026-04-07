from core.state import ZypState

def main():
    state = ZypState(goal="bootstrap ZYPHOS")
    print("ZYPHOS STATE:")
    print(state.model_dump())

if __name__ == "__main__":
    main()
