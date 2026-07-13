import { useAuth } from "../context/AuthContext.jsx";

export default function Profile() {
  const { user } = useAuth();

  return (
    <div className="max-w-md mx-auto px-4 py-8">
      <div className="card space-y-4">
        <h1 className="text-xl font-semibold">Profile</h1>
        <div>
          <p className="text-sm text-gray-400">Name</p>
          <p className="font-medium">{user?.name}</p>
        </div>
        <div>
          <p className="text-sm text-gray-400">Email</p>
          <p className="font-medium">{user?.email}</p>
        </div>
        <div>
          <p className="text-sm text-gray-400">Member since</p>
          <p className="font-medium">{user?.created_at && new Date(user.created_at).toLocaleDateString()}</p>
        </div>
        <p className="text-xs text-gray-400 pt-2">
          Password changes and account settings can be wired up here against the backend's future
          `/auth/change-password` endpoint.
        </p>
      </div>
    </div>
  );
}
