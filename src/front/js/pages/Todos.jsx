import React, { useContext } from "react"
import { Context } from "../store/appContext"

const Todos = () => {
    const { store } = useContext(Context)

    return (
        <>
            <h1>Todos</h1>
            <img src={store.currentUser?.avatar} />

        </>
    )
}

export default Todos