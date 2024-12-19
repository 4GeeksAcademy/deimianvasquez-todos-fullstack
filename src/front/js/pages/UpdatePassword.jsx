import React, { useState, useContext } from "react";
import { Context } from "../store/appContext";
import { useSearchParams } from "react-router-dom";


const UpdatePassword = () => {
    const { actions } = useContext(Context)

    const [newPass, setNewPass] = useState("")

    const [searchParams, _] = useSearchParams()

    const handleSubmit = async (event) => {
        event.preventDefault()
        const updateToken = searchParams.get("token")

        const response = await actions.updatePassword(updateToken, newPass)
    }

    return (
        <div className="container">
            <div className="row justify-content-center">
                <h1 className="text-center">Actualizar contraseña de la app</h1>
                <div className="col-12 col-md-6 border py-4">
                    <form
                        onSubmit={handleSubmit}
                    >
                        <div className="form-group mb-3">
                            <label htmlFor="lblPass">Ingresar contraseña</label>
                            <input
                                type="password"
                                className="form-control"
                                placeholder="123456"
                                id="lblPass"
                                name="password"
                                value={newPass}
                                onChange={(event) => setNewPass(event.target.value)}
                            />
                        </div>
                        <button className="btn btn-outline-primary w-100">Recuperar contraseña</button>
                    </form>
                </div>
            </div>
        </div>
    )
}

export default UpdatePassword