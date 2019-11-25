db.createUser(
    {
        user: yanwan,
        pwd: <user-password>,
        roles: [
            {
                role: "readWrite",
                db: "cloudmesh"
            }
        ]
    }
);