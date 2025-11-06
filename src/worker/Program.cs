using System;
using System.Threading.Tasks;
using StackExchange.Redis;

class Program
{
    static async Task Main()
    {
        Console.WriteLine("Worker service started...");
        var redis = ConnectionMultiplexer.Connect(Environment.GetEnvironmentVariable("REDIS") ?? "redis");
        var db = redis.GetDatabase();

        while (true)
        {
            var vote = await db.ListLeftPopAsync("votes");
            if (!vote.IsNullOrEmpty)
            {
                string key = vote.ToString().ToLower() == "a" ? "cats" : "dogs";
await db.StringIncrementAsync(key);
                Console.WriteLine($"Processed vote: {vote}");
            }
            await Task.Delay(100);
        }
    }
}