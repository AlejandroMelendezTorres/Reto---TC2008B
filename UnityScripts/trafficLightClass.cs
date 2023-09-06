using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class trafficLightClass : MonoBehaviour
{
    public int id;
    int state;
    public GameObject[] lights;
    public Material[] materials;

    public void updateState(int i)
    {
        state = i;
    }

    // Start is called before the first frame update
    void Start()
    {
        lights[0].GetComponent<Renderer>().material = materials[3];
        lights[1].GetComponent<Renderer>().material = materials[3];
        lights[2].GetComponent<Renderer>().material = materials[2];
    }

    // Update is called once per frame
    void Update()
    {
        if (state == 0){
            lights[0].GetComponent<Renderer>().material = materials[0];
            lights[1].GetComponent<Renderer>().material = materials[3];
            lights[2].GetComponent<Renderer>().material = materials[3];
        }
        else if (state == 1){
            lights[0].GetComponent<Renderer>().material = materials[3];
            lights[1].GetComponent<Renderer>().material = materials[1];
            lights[2].GetComponent<Renderer>().material = materials[3];
        } else if (state == 2){
            lights[0].GetComponent<Renderer>().material = materials[3];
            lights[1].GetComponent<Renderer>().material = materials[3];
            lights[2].GetComponent<Renderer>().material = materials[2];
        } else {
            lights[0].GetComponent<Renderer>().material = materials[3];
            lights[1].GetComponent<Renderer>().material = materials[3];
            lights[2].GetComponent<Renderer>().material = materials[3]; 
        }
    }
}
