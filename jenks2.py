#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import json
import numpy as np



def finishPlot( fig, ax = None, fname = "finishPlot", loc='best', left = None, bottom = None, right = None, top = None, wspace = None, hspace = None, close = False ):
    """
    Give ax = [] in order to not draw a legend
    """
    fname = fname.replace( ":", "" )
    if ax is None:
        ax = fig.axes
    if not isinstance( ax, list):
        ax = [ ax ]
    for a in ax:
        # frameon = True necessary to work with seaborn
        l = a.legend( loc = loc, prop = {'size':10}, labelspacing = 0.2, # fontsize=10 also works
                      fancybox = True, framealpha = 0.5, frameon = True )
    #if l != None:
    #    l.set_zorder(0)  # alternative to transparency
    fig.tight_layout()
    fig.subplots_adjust( left = left, bottom = bottom, right = right, top = top, wspace = wspace, hspace = hspace )

    fig.savefig( fname+".pdf" )
    print( "[Saved '"+fname+".pdf']" )
    fig.savefig( fname+".png" )
    print( "[Saved '"+fname+".png']" )

    fig.canvas.set_window_title( fname )
    if close:
        plt.close( fig )



def get_jenks_breaks(data, lower_class_limits, nClasses):
    k = len(data) - 1
    kclass = [0.] * (nClasses+1)
    countNum = nClasses

    kclass[nClasses] = data[len(data) - 1]
    kclass[0] = data[0]

    while countNum > 1:
        elt = int(lower_class_limits[k][countNum] - 2)
        kclass[countNum - 1] = data[elt]
        k = int(lower_class_limits[k][countNum] - 1)
        countNum -= 1

    return kclass


def jenks2( data, nClasses ):
    # need at least 1 data point per class, obviously
    if nClasses > len( data ):
        return

    data = np.sort( data )

    #fill the matrices with data+1 arrays of nClasses 0s
    xi = np.zeros( [ len(data)+1, nClasses+1 ] )  # lower class limits
    vc = np.zeros( [ len(data)+1, nClasses+1 ] )  # variance combinations

    xi[1]  = 1
    #vc[1]  = 0
    vc[2:] = float('inf')

    variance = 0.0
    for l in range(2, len(data)+1):
        sum = 0.0
        sum_squares = 0.0
        w = 0.0
        for m in range(1, l+1):
            # `III` originally
            xinew = l - m + 1   # lower class limit
            val = data[xinew-1]

            # here we're estimating variance for each potential classing
            # of the data, for each potential number of classes. `w`
            # is the number of data points considered so far.
            w += 1

            # increase the current sum and sum-of-squares
            sum += val
            sum_squares += val * val

            # the variance at this point in the sequence is the difference
            # between the sum of squares and the total x 2, over the number
            # of samples.
            variance = sum_squares - (sum * sum) / w

            i4 = xinew - 1

            if i4 != 0:
                for j in range(2, nClasses+1):
                    if vc[l][j] >= (variance + vc[i4][j - 1]):
                        xi[l][j] = xinew
                        vc[l][j] = variance + vc[i4][j - 1]

        xi[l][1] = 1.
        vc[l][1] = variance

    # instead of returning indices, return y-values, this is basically what
    # get_jenks_breaks does, but it also has to read the table of the
    # algorithm steps correctly
    return get_jenks_breaks( data, xi, nClasses )


import matplotlib.pyplot as plt

def sma( x, n ):
    res = np.empty( len(x) )
    for i in range( len(x) ):
        i0 = max( 0, i - n//2 )
        i1 = min( len(x), i0 + n )
        res[i] = np.average( x[i0:i1] )
    return res

def test():
    #data = np.array( json.load(open('test.json')) )
    #mus    = [ 3  , 4.24, 8.13 ]
    #sigmas = [ 0.4, 0.6 , 1.1  ]
    mus    = [ 1, 3, 5, 2, 3 ]
    sigmas = [ 0.1, 0.1, 0.1, 0.01, 0.2  ]
    #ns     = [ 40, 60, 30, 50, 80 ]
    ns     = np.array([ 4,6,3,5,8 ])*3
    ns     = np.array([ 1,1,1,1,1 ])*10
    assert( len(mus) == len(sigmas) )
    assert( len(mus) == len(ns) )
    data = []
    for i in range( len( mus ) ):
        data = np.concatenate( [ data, np.random.normal( mus[i], sigmas[i], ns[i]) ] )
    data = sma( data, 5 )

    breaks = [ np.min( data ) ]
    for i in range(len(mus)-1):
        breaks += [ mus[i] + ( mus[i+1]-mus[i] )/( sigmas[i] + sigmas[i+1] ) * sigmas[i] ]
    breaks += [ np.max( data ) ]

    print( "I roughly would expect the partitions to be at:\n" + str( breaks ) )


    for i in range(2,6):
        print( jenks2( data, i ) )
    breaks = jenks2( data, 3 )

    fig = plt.figure( figsize=(10,5) )
    axf = fig.add_subplot(131)
    axf.plot( data, 'o' )
    axh = fig.add_subplot(132)
    axh.hist( data, bins = 20 )
    for br in breaks:
        axh.axvline( br, color = 'r' )
        axf.axhline( br, color = 'r' )

    # Plot
    ax = fig.add_subplot(133)
    finishPlot( fig, fname = "natural-break-example" )
    plt.show()

import csv
def main():
    # https://docs.python.org/2.4/lib/standard-encodings.html
    # https://www.bundeswahlleiter.de/bundestagswahlen/2017/wahlkreiseinteilung/umgerechnete-ergebnisse.html
    #  -> https://www.bundeswahlleiter.de/dam/jcr/36efa904-5d4a-4159-a11e-2c8ecc1b0f77/btwkr17_umrechnung_btw13.csv
    with open( 'btwkr17_umrechnung_btw13.csv', newline='', encoding='ISO8859-15' ) as csvfile:
        spamreader = csv.reader( csvfile, delimiter=';' )
        # Wkr-Nr.;Land;Wahlkreisname;Wahlberechtigte;Wähler;Ungültige;Ungültige;Gültige;Gültige;CDU;CDU;SPD;SPD;FDP;FDP;DIE LINKE;DIE LINKE;GRÜNE;GRÜNE;CSU;CSU;PIRATEN;PIRATEN;NPD;NPD;Tierschutzpartei;Tierschutzpartei;REP;REP;ÖDP;ÖDP;FAMILIE;FAMILIE;Bündnis 21/RRP;Bündnis 21/RRP;RENTNER;RENTNER;BP;BP;PBC;PBC;BüSo;BüSo;DIE VIOLETTEN;DIE VIOLETTEN;MLPD;MLPD;Volksabstimmung;Volksabstimmung;PSG;AfD;AfD;BIG;BIG;pro Deutschland;pro Deutschland;DIE RECHTE;DIE FRAUEN;FREIE WÖHLER;FREIE WÖHLER;Nichtwähler;PARTEI DER VERNUNFT;PARTEI DER VERNUNFT;Die PARTEI;Die PARTEI;Bergpartei;BGD;DKP;NEIN!;WGr/EB
        # ;;;;;Erststimmen;Zweitstimmen;Erststimmen;Zweitstimmen;Erststimmen;Zweitstimmen;Erststimmen;Zweitstimmen;Erststimmen;Zweitstimmen;Erststimmen;Zweitstimmen;Erststimmen;Zweitstimmen;Erststimmen;Zweitstimmen;Erststimmen;Zweitstimmen;Erststimmen;Zweitstimmen;Erststimmen;Zweitstimmen;Erststimmen;Zweitstimmen;Erststimmen;Zweitstimmen;Erststimmen;Zweitstimmen;Erststimmen;Zweitstimmen;Erststimmen;Zweitstimmen;Erststimmen;Zweitstimmen;Erststimmen;Zweitstimmen;Erststimmen;Zweitstimmen;Erststimmen;Zweitstimmen;Erststimmen;Zweitstimmen;Erststimmen;Zweitstimmen;Zweitstimmen;Erststimmen;Zweitstimmen;Erststimmen;Zweitstimmen;Erststimmen;Zweitstimmen;Zweitstimmen;Zweitstimmen;Erststimmen;Zweitstimmen;Zweitstimmen;Erststimmen;Zweitstimmen;Erststimmen;Zweitstimmen;Erststimmen;Erststimmen;Erststimmen;Erststimmen;Erststimmen
           # -> let's not parse this, let's just know that

        header    = None
        stimminfo = None
        data = []
        for row in spamreader:
            if len( row ) < 1:
                continue
            if len(row[0]) >= 1 and row[0][0] == '#':
                continue

            if header is None and len( row[-1] ) > 0:
                header = row
            elif stimminfo is None:
                stimminfo = row
            elif row[0].isdigit():
                data += [ row ]
                #print( ', '.join( row ) )

        hasDirect = {}
        hasSecond = {}
        for i in range( min( len( header ), len( stimminfo ) ) ):
            if stimminfo[i] == 'Erststimmen':
                hasDirect[ header[i] ] = True
            elif stimminfo[i] == 'Zweitstimmen':
                hasSecond[ header[i] ] = True

        print( header )
        iCol = {}
        for i in range( len( header ) ):
            # each party is two listed two times, we only want the first index for them
            if not header[i] in iCol:
                iCol[ header[i] ] = i
                #print( i,"->",header[i] )


        parties = [ 'CDU', 'SPD', 'FDP', 'DIE LINKE', 'GRÜNE', 'AfD' ]
        colors = {
            'CDU'       : [ 'f7f7f7', 'cccccc', '969696', '525252' ],   # black
            'SPD'       : [ 'fee5d9', 'fcae91', 'fb6a4a', 'cb181d' ],   # red
            'FDP'       : [ 'ffffd4', 'fed98e', 'fe9929', 'cc4c02' ],   # yellow / orange
            'DIE LINKE' : [ 'f1eef6', 'd7b5d8', 'df65b0', 'ce1256' ],   # magenta
            'GRÜNE'     : [ 'edf8fb', 'b2e2e2', '66c2a4', '238b45' ],   # green
            'AfD'       : [ 'eff3ff', 'bdd7e7', '6baed6', '2171b5' ],   # blue
        }

        figParties       = plt.figure( figsize = ( 8,8 ) )
        figPartiesSorted = plt.figure( figsize = ( 8,8 ) )

        for iParty in range( len( parties ) ):
            party = parties[ iParty ]
            if not party in iCol:
                print( "Warning, couldn't find '" + party + "' in data." )
                continue

            # well, could use list instead of hardcoded 299 here, but oh well
            nKreise = 299
            res1 = np.zeros( nKreise )
            res2 = np.zeros( nKreise )
            for row in data:
                iKreis = int( row[0] )-1
                if iKreis > nKreise:
                    continue

                if hasDirect[ party ]:
                    res1[ iKreis ] = int( row[ iCol[ party ] + 0 ] ) / \
                                     int( row[ iCol[ 'Gültige' ] + 0 ] )
                    if party == 'CDU':
                        res1[ iKreis ] += int( row[ iCol[ 'CSU' ] + 0 ] ) / \
                                          int( row[ iCol[ 'Gültige' ] + 0 ] )

                if hasSecond[ party ]:
                    res2[ iKreis ] = int( row[ iCol[ party ] + hasDirect[ party ] ] ) / \
                                     int( row[ iCol[ 'Gültige' ] + 1 ] )
                    if party == 'CDU':
                        res2[ iKreis ] += int( row[ iCol[ 'CSU' ] + hasDirect[ party ] ] ) / \
                                          int( row[ iCol[ 'Gültige' ] + 1 ] )

                #print( res1[ iKreis ], res2[ iKreis ] )
                #print( row[ iCol['Gültige']+0 ], np.sum( np.array( [ int(x) for x in row[ iCol['Gültige']+0+2::2 ] ] ) ) )
                #print( row[ iCol['Gültige']+1 ], np.sum( np.array( [ int(x) for x in row[ iCol['Gültige']+1+2::2 ] ] ) ) )

            print( party,"Results:", 100*res1[33], 100*res2[33] )

            # find color levels and plot distribution of percentages
            ax  = figParties      .add_subplot( 3, 2, 1+iParty, title = party, ylabel = "%", xlabel = "Wahlbezirk" )
            ax.plot( 100 * res2 )
            ax  = figPartiesSorted.add_subplot( 3, 2, 1+iParty, title = party, ylabel = "%", xlabel = "Platzierung" )
            ax.plot( 100 * np.sort( res2 ) )

            levels = np.array( jenks2( np.sort( res2 ), 4 ) )
            print( party, "Levels:", levels )
            print( party, "Levels:", 100 * levels )

            # Write out css file:
            with open( "kreise." + party + ".svg", 'w' ) as cssFile:
                for iKreis in range( len( res2 ) ):
                    iLevel = np.searchsorted( levels, res2[ iKreis ] ) - 1
                    print( res2[iKreis], iLevel )
                    cssFile.write( ".kreis" + str( iKreis+1 ) + " { fill: #" + colors[ party ][iLevel] + "; }" )

        finishPlot( figParties, fname = "parties" )
        finishPlot( figPartiesSorted, fname = "parties-distributions" )


if __name__ == "__main__":
    main()
