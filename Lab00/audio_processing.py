
def backwards(sound):
    """
    Parameters: sound, dict

    sound is a representation of mono sound
    rate, int, units of samples per second
    samples, list, list of samples, floats

    returns reverse sound

    # does not modify the original sound
    """

    sound_copy = sound.copy()    # makes a copy of the dictionary
    samples_copy = sound_copy["samples"].copy() # makes a copy of the samples
    samples_copy_rev = samples_copy[::-1]  # updates the value of samples to reversed list
        
    sound_copy["samples"] = samples_copy_rev
    
    return sound_copy   # returns a copy of the reversed samples

def mix(sound1, sound2, p):
    """
    Parameters:
        sound1- dict, contains keys: rate, samples and values: int, list of floats
        sound2 - same as above
        p- float 0<= p <=1

        Return:
            copy of new sound that is combination of sound1["samples"]*p + sound2["samples"]*p
        with a duration of the shorter sound
        # Note: the original sounds need to be unchanged
    """
    # initialization section
    sound1_copy = sound1.copy()
    sound2_copy = sound2.copy()
    new_sound = {}
    
    new_sound["rate"] = sound1_copy["rate"]
    new_sound["samples"] = []
    
    # checks for different sampling rates
    if sound1["rate"] != sound2["rate"]:
        return None
    
    # sound1 has a shorter duration
    if len(sound1["samples"]) < len(sound2["samples"]):

        # mixing copy of sounds                         
        for index, val in enumerate(list(sound1_copy["samples"])):
            # val is each sample in sound1
            # combining samples after multiplying mixing parameter
            sample_comb = (val*p)+ (sound2_copy["samples"][index]* (1-p))

            new_sound["samples"].append(sample_comb)# adding mixed sample 
            
    # sound2 has a shorter duration
    elif len(sound2["samples"]) < len(sound1["samples"]):

        # mixing copy of sounds
        for index, val in enumerate(list(sound2_copy["samples"])):
            # val is each sample in sound2
            # combining samples after multiplying mixing parameter
            sample_comb = (val*(1-p))+(sound1_copy["samples"][index]*p)
                                
            new_sound["samples"].append(sample_comb)
    
    return new_sound    # returns a new sound from the mixing of the two sounds

def echo(sound, num_echoes, delay, scale):
    """
    Parameters:
        sound- dict, contains rate: int, samples: list of floats
        num_echoes- int, number of additional copies of sound
        delay- float, # of seconds between echo
        scale- float, amount to scale each echo
                (each additional copy will be have scale applied again)
        
    Task:
        create echo effect for samples by adding a delay and scaling samples
    for a specified echo
        
    Return:
        new sound with echo effect
        
    """
    echo_sound = sound.copy()
    sample_delay = round(delay*sound["rate"])
    
    # makes an empty array of zeros
    echo_list_copy = [0] * (num_echoes*sample_delay+ len(echo_sound["samples"]))
    
    # number of echoes
    for num in range(num_echoes+1):
        
        # index of where echo starts
        index = sample_delay*num
       
        # scale each sample to become an echo effect
        for sample in echo_sound["samples"]:
            scaled = scale**num   # scale factor for corresponding echo
            echo_list_copy[index] += scaled*sample # adds the scaled echo effect
            index+=1  # updates the index
            
    echo_sound["samples"] = echo_list_copy      # updates the copied sound to have echo effect

    return echo_sound    # returns the echo sound

def pan(sound):
    """
    Parameters:
        sound- dict, rate:int, 
               left: list of left speaker samples,
               right: list of right speaker samples
        
    Return:
        scale a copy of the left and right speaker samples
    """
    pan_sound = sound.copy()
    right = pan_sound["right"].copy()
    left = pan_sound["left"].copy()
    length = len(right)
    
    # scaling the left and right speakers
    for index, sample in enumerate(right):
        left[index] *= (1- index/(length-1))
        right[index] = sample*(index/(length-1))
        
    pan_sound["left"] = left        # updates the left speaker samples  
    pan_sound["right"] = right      # updates the right speaker samples
    
    return pan_sound  # returns a scaled left and right speaker

def remove_vocals(sound):
    """
    Parameters:
        sound- dict, rate:int, 
               left: list of left speaker samples,
               right: list of right speaker samples
    Task:
        find the difference between left and right samples
    to remove vocals
    
    Return:
        new mono sound that removes the vocals and doesn't modify the original sound
    """
    # initialization section
    remove_sound = {}
    #remove_vocal = []
    
    sound_copy = sound.copy()
    left = sound_copy["left"]
    right = sound_copy["right"]
    
    remove_sound["rate"] = sound_copy["rate"]
    remove_sound["samples"] = []
    
    # finds difference for all left and right samples
    for index, sample in enumerate(left):
        diff = sample - right[index]    # finds difference between left and right sample
        remove_sound["samples"].append(diff)     # adds the removed vocal to listen
    
    return remove_sound

# below are helper functions for converting back-and-forth between WAV files
# and our internal dictionary representation for sounds

import io
import wave
import struct


def load_wav(filename, stereo=False):
    """
    Given the filename of a WAV file, load the data from that file and return a
    Python dictionary representing that sound
    """
    f = wave.open(filename, "r")
    chan, bd, sr, count, _, _ = f.getparams()

    assert bd == 2, "only 16-bit WAV files are supported"

    out = {"rate": sr}

    if stereo:
        left = []
        right = []
        for i in range(count):
            frame = f.readframes(1)
            if chan == 2:
                left.append(struct.unpack("<h", frame[:2])[0])
                right.append(struct.unpack("<h", frame[2:])[0])
            else:
                datum = struct.unpack("<h", frame)[0]
                left.append(datum)
                right.append(datum)

        out["left"] = [i / (2**15) for i in left]
        out["right"] = [i / (2**15) for i in right]
    else:
        samples = []
        for i in range(count):
            frame = f.readframes(1)
            if chan == 2:
                left = struct.unpack("<h", frame[:2])[0]
                right = struct.unpack("<h", frame[2:])[0]
                samples.append((left + right) / 2)
            else:
                datum = struct.unpack("<h", frame)[0]
                samples.append(datum)

        out["samples"] = [i / (2**15) for i in samples]

    return out


def write_wav(sound, filename):
    """
    Given a dictionary representing a sound, and a filename, convert the given
    sound into WAV format and save it as a file with the given filename (which
    can then be opened by most audio players)
    """
    outfile = wave.open(filename, "w")

    if "samples" in sound:
        # mono file
        outfile.setparams((1, 2, sound["rate"], 0, "NONE", "not compressed"))
        out = [int(max(-1, min(1, v)) * (2**15 - 1)) for v in sound["samples"]]
    else:
        # stereo
        outfile.setparams((2, 2, sound["rate"], 0, "NONE", "not compressed"))
        out = []
        for l, r in zip(sound["left"], sound["right"]):
            l = int(max(-1, min(1, l)) * (2**15 - 1))
            r = int(max(-1, min(1, r)) * (2**15 - 1))
            out.append(l)
            out.append(r)

    outfile.writeframes(b"".join(struct.pack("<h", frame) for frame in out))
    outfile.close()


if __name__ == "__main__":
    # code in this block will only be run when you explicitly run your script,
    # and not when the tests are being run.  this is a good place to put your
    # code for generating and saving sounds, or any other code you write for
    # testing, etc.

    # here is an example of loading a file (note that this is specified as
    # sounds/meow.wav, rather than just as meow.wav, to account for the sound
    # files being in a different directory than this file)
    meow = load_wav("sounds/meow.wav")

    # write_wav(backwards(meow), 'meow_reversed.wav')

    # creating reversed mystery sound  
    mystery = load_wav("sounds/mystery.wav")
    write_wav(backwards(mystery), "mystery_rev.wav")
    
    # creating mixed sound
    synth = load_wav("sounds/synth.wav")
    water = load_wav("sounds/water.wav")
    write_wav(mix(synth, water, 0.2), "mixed.wav")
    
    # creating an echo effect with the sound
    chord = load_wav("sounds/chord.wav")
    write_wav(echo(chord, 5, 0.3, 0.6), "echo.wav")
    
    # creating a stereo effect with the sound
    car = load_wav("sounds/car.wav", stereo=True)
    write_wav(pan(car), "pan.wav")

    # creating a sound with removed vocals
    rem_voc = load_wav("sounds/lookout_mountain.wav", stereo=True)
    write_wav(remove_vocals(rem_voc), "removed_vocals.wav")
