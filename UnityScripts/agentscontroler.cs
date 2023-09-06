using System.Collections;
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;
using UnityEngine.Networking;
using SimpleJSON;

public class AgentController : MonoBehaviour
{

    public JSONNode userData;

    //public GameObject carPrefab;
    
    public GameObject carPrefab1;
    public GameObject carPrefab2;
    public GameObject carPrefab3;
    public GameObject carPrefab4;
    public GameObject carPrefab5;
    public GameObject carPrefab6;
    List<GameObject> carPrefabs = new List<GameObject>();


    Dictionary<int, GameObject> carAgents = new Dictionary<int, GameObject>();

    Dictionary<int, Vector3> carPositions;
    Dictionary<int, Vector3> newCarPositions = new Dictionary<int, Vector3>();

    Dictionary<int, Vector2> directions = new Dictionary<int, Vector2>();

    public float timeToUpdate = 5.0f;
    private float timer;
    float dt;

    // IEnumerator - yield return
    IEnumerator SendData(string data)
    {
        WWWForm form = new WWWForm();
        form.AddField("bundle", "the data");
        string url = "http://localhost:8585";
        //Send the request then wait here until it returns
        using (UnityWebRequest www = UnityWebRequest.Post(url, form))
        {
            byte[] bodyRaw = System.Text.Encoding.UTF8.GetBytes(data);
            www.uploadHandler = (UploadHandler)new UploadHandlerRaw(bodyRaw);
            www.downloadHandler = (DownloadHandler)new DownloadHandlerBuffer();
            www.SetRequestHeader("Content-Type", "application/json");

            yield return www.SendWebRequest();          // Talk to Python
            // Now we check for errors
            if (www.isNetworkError || www.isHttpError)
            {
                Debug.Log(www.error);
            }
            else
            {
                //Process the response
                userData = SimpleJSON.JSON.Parse(www.downloadHandler.text);
                //Debug.Log(userData);
                //List<Vector3> newPositions = new List<Vector3>();

                //get the number of objects in the data array
                int numOfObjects = userData["data"].Count;
                newCarPositions.Clear();

                //Create a list of the positions for each agent

                for (int i = 0; i < numOfObjects; i++)
                {
                    int id = userData["data"][i]["ID"];
                    //Debug.Log(userData["data"][i]);
                    float x = userData["data"][i]["x"];
                    float y = userData["data"][i]["y"];
                    float z = userData["data"][i]["z"];

                    // Get gameobject by name
                    Vector3 pos = new Vector3(x, y, z);

                    if (userData["data"][i]["type"] == 0)//if the object is a car
                    {
                        Vector2 dir = new Vector2(userData["data"][i]["Dirx"], userData["data"][i]["Diry"]);
                        //newPositions.Add(pos);
                        newCarPositions[id] = pos;
                        directions[id] = dir;
                    }
                    else if (userData["data"][i]["type"] == 1)//if the object is a trafic light
                    {
                        GameObject trafficlight = GameObject.Find(userData["data"][i]["ID"].ToString());
                        // Get the trafficlightClass script from the trafficlight
                        trafficlight.GetComponent<trafficLightClass>().updateState(userData["data"][i]["color"]);
                    }
                }
                //positions.Add(newPositions);
            }
        }
        //Debug.Log("Done");
        yield return null;
    }

    // Start is called before the first frame update
    IEnumerator Start()
    {
        
        //Innit the car prefabs
        carPrefabs.Add(carPrefab1);
        carPrefabs.Add(carPrefab2);
        carPrefabs.Add(carPrefab3);
        carPrefabs.Add(carPrefab4);
        carPrefabs.Add(carPrefab5);
        carPrefabs.Add(carPrefab6);
        

        //Get the first data from Python
        string json = EditorJsonUtility.ToJson("");
        yield return StartCoroutine(SendData(json));
        timer = timeToUpdate;
        InnitAgents();
    }

    // Update is called once per frame
    void Update()
    {

        timer -= Time.deltaTime;
        dt = 1.0f - (timer / timeToUpdate);

        if (timer < 0)
        {
            _ = StartCoroutine(UpdateData());
            timer = timeToUpdate;
        }


    }
    IEnumerator UpdateData()
    {
        //Debug.Log("Update");
        string json = EditorJsonUtility.ToJson("");
        yield return StartCoroutine(SendData(json));
        UpdateCars();
    }

    void InnitAgents()
    {
        //Create the cars
        carPositions = new Dictionary<int, Vector3>(newCarPositions);

        foreach (var carPosition in carPositions)
        {
            //choose ramndomly a car prefab
            int carPrefabIndex = UnityEngine.Random.Range(0, carPrefabs.Count);
            GameObject carPrefab = carPrefabs[carPrefabIndex];

            //Instantiate the car
            Vector3 pos = carPositions[carPosition.Key];
            int x = (int)pos.x;
            int y = (int)pos.z;
            GameObject temp = GameObject.Find(x+"x"+y);
            GameObject newCar = Instantiate(carPrefab, temp.transform.position, Quaternion.identity);
            carAgents[carPosition.Key] = newCar;
        }

    }

    void UpdateCars()
    {
        //check if the car exists in carPositions
        foreach (var car in newCarPositions)
        {
            string name = "";
            string xtemp = "x";
            // convert x float into int
            int x = (int)car.Value.x;

            int y = (int)car.Value.z;

            name = x + xtemp + y;

            Vector2 dir = directions[car.Key];

            //name = x.ToString() + "x" + y.ToString();
            

            GameObject carAgent = GameObject.Find(name);


            //if the car exists both in new and existing cars, update its position
            if (carPositions.ContainsKey(car.Key))
            {
                //Debug.Log("Update car");
                //carAgents[car.Key].transform.position = Vector3.Lerp(carPositions[car.Key], car.Value, dt);
                if (carAgent != null){
                    carAgents[car.Key].transform.position = carAgent.transform.position;
                    // Move towards the target
                    //carAgents[car.Key].transform.position = Vector3.MoveTowards(carAgents[car.Key].transform.position, carAgent.transform.position, Time.deltaTime * 50);
                }
                else {
                    carAgents[car.Key].transform.position = car.Value;
                }
                carPositions[car.Key] = car.Value;
            }
            //if the car doesn't exist in carPositions, but it exists in newCarPositions, create it
            else
            {
                //if the car doesn't exist, create it
                //choose ramndomly a car prefab
                int carPrefabIndex = UnityEngine.Random.Range(0, carPrefabs.Count);
                GameObject carPrefab = carPrefabs[carPrefabIndex];

                //Instantiate the car
                //Debug.Log("Create new car");
                if (carAgent != null){
                    GameObject newCar = Instantiate(carPrefab, carAgent.transform.position, Quaternion.identity);
                    carAgents[car.Key] = newCar;
                    carPositions[car.Key] = car.Value;
                } else {
                    GameObject newCar = Instantiate(carPrefab, car.Value, Quaternion.identity);
                    carAgents[car.Key] = newCar;
                    carPositions[car.Key] = car.Value;
                } 
                
            }

            int k = (int) dir.x;
            int u = (int) dir.y;

            if (x == 10 && y == 10){
                try{
                    GameObject carAgent2 = GameObject.Find("9x11");
                    carAgents[car.Key].transform.LookAt(carAgent2.transform);
                    carAgents[car.Key].transform.Rotate(0, 180, 0);
                } catch{}
            } else if (x == 10 && y == 13){
                try{
                    GameObject carAgent2 = GameObject.Find("11x14");
                    carAgents[car.Key].transform.LookAt(carAgent2.transform);
                    carAgents[car.Key].transform.Rotate(0, 180, 0);
                } catch{}
            } else if (x == 13 && y == 10){
                try{
                    GameObject carAgent2 = GameObject.Find("12x9");
                    carAgents[car.Key].transform.LookAt(carAgent2.transform);
                    carAgents[car.Key].transform.Rotate(0, 180, 0);
                } catch{}
            } else if (x == 13 && y == 13){
                try{
                    GameObject carAgent2 = GameObject.Find("14x12");
                    carAgents[car.Key].transform.LookAt(carAgent2.transform);
                    carAgents[car.Key].transform.Rotate(0, 180, 0);
                } catch{}
            } else {
                try{
                    GameObject carAgent2 = GameObject.Find((x+k)+"x"+(y+ u));
                    carAgents[car.Key].transform.LookAt(carAgent2.transform);
                } catch{}
            }
        }
        //if the car doesn't exist in newCarPositions, but it exists in carPositions, destroy it
        List<int> carsToDestroy = new List<int>();
        foreach (var car2 in carPositions)
        {
            if (!newCarPositions.ContainsKey(car2.Key))
            {
                //Debug.Log("Car to destroy: "+car2.Key);
                carsToDestroy.Add(car2.Key);
            }
        }
        foreach (var car3 in carsToDestroy)
        {
            //Debug.Log("Destroy car");
            Destroy(carAgents[car3]);
            carAgents.Remove(car3);
            carPositions.Remove(car3);
        }
    }

}
