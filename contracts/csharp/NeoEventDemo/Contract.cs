using Neo;
using Neo.SmartContract;
using Neo.SmartContract.Framework;
using Neo.SmartContract.Framework.Attributes;
using Neo.SmartContract.Framework.Services;
using System;

namespace csharp
{
    [ManifestExtra("name", "NeoEventDemo")]
    [ContractAuthor("Chimaobi", "chimaemekaiheonu@example.com")]
    [ContractDescription("A simple event-based Neo N3 demo contract")]
    public class Contract : SmartContract
    {
        public static event Action<UInt160, string> OnPing;

        [Safe]
        public static bool Trigger(UInt160 sender, string message)
        {
            OnPing(sender, message);
            return true;
        }
    }
}
